#include <Python.h>
#include <iostream>
#include <stdio.h>
#include <alsa/asoundlib.h>
#include "edge-impulse-sdk/classifier/ei_run_classifier.h"
#include <cstring> // For memset

// Callback function to fetch audio data
static int get_signal_data(size_t offset, size_t length, float *out_ptr);

// Audio capture settings
#define PCM_DEVICE "default"
unsigned int AUDIO_SAMPLE_RATE = 16000;  // Removed const to allow passing the address
#define AUDIO_FRAME_SIZE EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE

// Buffer to store captured audio
static float audio_buffer[AUDIO_FRAME_SIZE];
static float noise_reference[AUDIO_FRAME_SIZE]; // Reference noise signal
static double filter_weights[50] = {0.0};       // LMS filter weights

// LMS filter function
void lms_filter(const float *input, const float *reference, float *output, double *weights, int filter_len, int signal_len, double mu) {
    memset(weights, 0, sizeof(double) * filter_len); // Initialize weights to zero

    for (int n = 0; n < signal_len; ++n) {
        double y = 0.0;

        // Compute filter output
        for (int k = 0; k < filter_len; ++k) {
            if (n >= k) {
                y += weights[k] * reference[n - k];
            }
        }

        // Calculate error
        double error = input[n] - y;
        output[n] = (float)error;

        // Update weights
        for (int k = 0; k < filter_len; ++k) {
            if (n >= k) {
                weights[k] += 2 * mu * error * reference[n - k];
            }
        }
    }
}

// Function to capture audio and perform inference
int capture_audio_and_infer(float previous_value, float current_value);

int main(int argc, char **argv) {
    float previous_value = 0.0;
    float current_value = 0.0;

    while (1) {
        int res = capture_audio_and_infer(previous_value, current_value);
        if ((res != 0) && (res != 1)) {
            printf("Audio capture or inference failed.\n");
            return 1;
        } else if (res == 1) {
            char path[] = "../command/main.py";
            FILE *file;
            Py_Initialize();

            file = fopen(path, "r");

            if (file == NULL)
                return -1;

            PyRun_SimpleFile(file, path);

            fclose(file);

            Py_Finalize();

            break;
        }

        previous_value = current_value;
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

    // Allocate hardware parameters object
    snd_pcm_hw_params_alloca(&params);

    // Set hardware parameters
    snd_pcm_hw_params_any(pcm_handle, params);
    snd_pcm_hw_params_set_access(pcm_handle, params, SND_PCM_ACCESS_RW_INTERLEAVED);
    snd_pcm_hw_params_set_format(pcm_handle, params, SND_PCM_FORMAT_S16_LE); // 16-bit audio
    snd_pcm_hw_params_set_channels(pcm_handle, params, 1);                  // Mono channel
    snd_pcm_hw_params_set_rate_near(pcm_handle, params, &AUDIO_SAMPLE_RATE, 0); // Pass the address of AUDIO_SAMPLE_RATE
    snd_pcm_hw_params_set_period_size_near(pcm_handle, params, &frames, 0);

    // Write the parameters
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

    // Convert the short buffer to float and store in audio_buffer
    for (size_t i = 0; i < buffer_size; i++) {
        audio_buffer[i] = (float)buffer[i] / 32768.0f; // Normalize 16-bit integer to float [-1, 1]
        noise_reference[i] = (float)(rand() % 32768) / 32768.0f - 0.5f; // Simulated reference noise
    }

    // Apply LMS filter to reduce noise
    float filtered_signal[AUDIO_FRAME_SIZE];
    lms_filter(audio_buffer, noise_reference, filtered_signal, filter_weights, 50, buffer_size, 0.01);

    // Run Edge Impulse inference
    signal_t signal;
    ei_impulse_result_t result;
    EI_IMPULSE_ERROR res;

    signal.total_length = AUDIO_FRAME_SIZE;
    signal.get_data = &get_signal_data;

    res = run_classifier(&signal, &result, false);

    // Print the inference results
    printf("Inference result: %d\n", res);
    printf("Timing: DSP %d ms, inference %d ms, anomaly %d ms\n",
           result.timing.dsp, result.timing.classification, result.timing.anomaly);

    current_value = result.classification[1].value;
    for (uint16_t i = 0; i < EI_CLASSIFIER_LABEL_COUNT; i++) {
        printf("%s: %.5f\n", ei_classifier_inferencing_categories[i], result.classification[i].value);
    }

    free(buffer);
    snd_pcm_close(pcm_handle);

    if (current_value > 0.89)
        return 1;

    return 0;
}

// Callback function to provide audio data for inference
static int get_signal_data(size_t offset, size_t length, float *out_ptr) {
    for (size_t i = 0; i < length; i++) {
        out_ptr[i] = audio_buffer[offset + i];
    }
    return EIDSP_OK;
}
