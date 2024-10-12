#include <stdio.h>
#include <alsa/asoundlib.h>
#include "edge-impulse-sdk/classifier/ei_run_classifier.h"

// Callback function to fetch audio data
static int get_signal_data(size_t offset, size_t length, float *out_ptr);

// Audio capture settings
#define PCM_DEVICE "default"
unsigned int AUDIO_SAMPLE_RATE = 16000;  // Removed const to allow passing the address
#define AUDIO_FRAME_SIZE EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE

// Buffer to store captured audio
static float audio_buffer[AUDIO_FRAME_SIZE];

// Function to capture audio and perform inference
int capture_audio_and_infer();

int main(int argc, char **argv) {
    while (1) {
        if (capture_audio_and_infer() != 0) {
            printf("Audio capture or inference failed.\n");
            return 1;
        }
    }
    return 0;
}

// Function to capture audio and run inference
int capture_audio_and_infer() {
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
    snd_pcm_hw_params_set_channels(pcm_handle, params, 1); // Mono channel
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
    }

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

    for (uint16_t i = 0; i < EI_CLASSIFIER_LABEL_COUNT; i++) {
        printf("%s: %.5f\n", ei_classifier_inferencing_categories[i], result.classification[i].value);
    }

    free(buffer);
    snd_pcm_close(pcm_handle);

    return 0;
}

// Callback function to provide audio data for inference
static int get_signal_data(size_t offset, size_t length, float *out_ptr) {
    for (size_t i = 0; i < length; i++) {
        out_ptr[i] = audio_buffer[offset + i];
    }
    return EIDSP_OK;
}
