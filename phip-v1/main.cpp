#include <Python.h>
#include <signal.h>
#include <time.h>
#include <stdio.h>
#include <alsa/asoundlib.h>
#include "edge-impulse-sdk/classifier/ei_run_classifier.h"

// Callback function to fetch audio data
static int get_signal_data(size_t offset, size_t length, float *out_ptr);

// Audio capture settings
#define PCM_DEVICE "default"
unsigned int AUDIO_SAMPLE_RATE = 16000;
#define AUDIO_FRAME_SIZE EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE

// Buffer to store captured audio
static float audio_buffer[AUDIO_FRAME_SIZE];

// Shared variables
volatile int run_python_script = 0;
float previous_value = 0.0, current_value = 0.0;

// Function to capture audio and perform inference
int capture_audio_and_infer(float previous_value, float current_value);

// Timer handler function
void timer_handler(int signum) {
    if (run_python_script) return; // Skip inference if Python is running
    int res = capture_audio_and_infer(previous_value, current_value);
    if (res == 1) {
        run_python_script = 1; // Signal main loop to run Python script
    }
}

int main(int argc, char **argv) {
    while (1) {
    // Configure timer
    struct sigaction sa;
    struct itimerspec timer_spec;
    timer_t timer_id;

    // Set up signal handler for SIGALRM
    sa.sa_flags = SA_RESTART;
    sa.sa_handler = timer_handler;
    sigaction(SIGRTMIN, &sa, NULL);

    // Create timer
    struct sigevent sev;
    sev.sigev_notify = SIGEV_SIGNAL;
    sev.sigev_signo = SIGRTMIN;
    sev.sigev_value.sival_ptr = &timer_id;
    timer_create(CLOCK_REALTIME, &sev, &timer_id);

    // Start timer: every 700ms
    timer_spec.it_value.tv_sec = 0;
    timer_spec.it_value.tv_nsec = 500 * 1000000; // 700ms
    timer_spec.it_interval.tv_sec = 0;
    timer_spec.it_interval.tv_nsec = 500 * 1000000; // 700ms
    timer_settime(timer_id, 0, &timer_spec, NULL);

    while (1) {
        if (run_python_script) {
            // Run Python script
            printf("Running main.py...\n");
            char path[] = "command/main.py"; // Assuming main.py is in the same directory as main.cpp
            FILE *file;
            Py_Initialize();
            file = fopen(path, "r");
            if (file == NULL) {
                perror("Failed to open main.py");
                return 1;
            }
            PyRun_SimpleFile(file, path);
            fclose(file);
            Py_Finalize();
            printf("main.py completed.\n");
            // Reset state for restarting inference
            run_python_script = 0;
        }
        //usleep(10); // Poll to avoid busy waiting
    }
    }
    return 0;
}

// Function to capture audio and run inference
int capture_audio_and_infer(float previous_value, float current_value) {
    snd_pcm_t *pcm_handle;
    snd_pcm_hw_params_t *params;
    int pcm, pcm_rc;
    short *buffer;
    snd_pcm_uframes_t frames;
    size_t buffer_size = AUDIO_FRAME_SIZE;

    // Allocate buffer for microphone input
    buffer = (short *)malloc(buffer_size * sizeof(short));
    if (!buffer) {
        printf("Failed to allocate audio buffer\n");
        return -1;
    }

    // Open the PCM device for recording
    if ((pcm = snd_pcm_open(&pcm_handle, PCM_DEVICE, SND_PCM_STREAM_CAPTURE, 0)) < 0) {
        printf("ERROR: Can't open PCM device. %s\n", snd_strerror(pcm));
        return -1;
    }

    // Configure PCM device
    snd_pcm_hw_params_alloca(&params);
    snd_pcm_hw_params_any(pcm_handle, params);
    snd_pcm_hw_params_set_access(pcm_handle, params, SND_PCM_ACCESS_RW_INTERLEAVED);
    snd_pcm_hw_params_set_format(pcm_handle, params, SND_PCM_FORMAT_S16_LE);
    snd_pcm_hw_params_set_channels(pcm_handle, params, 1);
    snd_pcm_hw_params_set_rate_near(pcm_handle, params, &AUDIO_SAMPLE_RATE, 0);
    snd_pcm_hw_params_set_period_size_near(pcm_handle, params, &frames, 0);
    if ((pcm = snd_pcm_hw_params(pcm_handle, params)) < 0) {
        printf("ERROR: Can't set hardware parameters. %s\n", snd_strerror(pcm));
        return -1;
    }

    // Capture audio data
    pcm_rc = snd_pcm_readi(pcm_handle, buffer, buffer_size);
    if (pcm_rc == -EPIPE) {
        printf("XRUN (overrun occurred).\n");
        snd_pcm_prepare(pcm_handle);
    } else if (pcm_rc < 0) {
        printf("ERROR: Can't read from PCM device. %s\n", snd_strerror(pcm_rc));
    } else if (pcm_rc != (int)buffer_size) {
        printf("Short read: read %d frames\n", pcm_rc);
    }

    // Convert audio data to float
    for (size_t i = 0; i < buffer_size; i++) {
        audio_buffer[i] = (float)buffer[i] / 32768.0f;
    }

    // Run inference
    signal_t signal;
    ei_impulse_result_t result;
    EI_IMPULSE_ERROR res;

    signal.total_length = AUDIO_FRAME_SIZE;
    signal.get_data = &get_signal_data;
    res = run_classifier(&signal, &result, false);

    // Print inference results
    printf("Inference result: %d\n", res);
    printf("Timing: DSP %d ms, inference %d ms, anomaly %d ms\n", 
           result.timing.dsp, result.timing.classification, result.timing.anomaly);
    current_value = result.classification[1].value;
    for (uint16_t i = 0; i < EI_CLASSIFIER_LABEL_COUNT; i++) {
        printf("%s: %.5f\n", ei_classifier_inferencing_categories[i], result.classification[i].value);
    }

    free(buffer);
    snd_pcm_close(pcm_handle);

    // Trigger condition for running main.py
    return (current_value > 0.49) ? 1 : 0;
}

// Callback function to provide audio data for inference
static int get_signal_data(size_t offset, size_t length, float *out_ptr) {
    for (size_t i = 0; i < length; i++) {
        out_ptr[i] = audio_buffer[offset + i];
    }
    return EIDSP_OK;
}
