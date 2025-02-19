# Tool macros
CC ?= gcc
CXX ?= g++

# Settings
NAME = phip
BUILD_PATH = ./build

# Location of main.cpp (must use C++ compiler for main)
CXXSOURCES = main.cpp
PYTHON_SCRIPT = main.py


# Search path for header files
CFLAGS += -I.
CFLAGS += -I./edge-impulse-sdk
CFLAGS += -I./model-parameters
CFLAGS += -I./tflite-model
CFLAGS += $(shell python3-config --includes)  # Include Python headers

# C and C++ Compiler flags
CFLAGS += -Wall						# Include all warnings
CFLAGS += -g						# Generate GDB debugger information
CFLAGS += -Wno-strict-aliasing		# Disable warnings about strict aliasing
CFLAGS += -Os						# Optimize for size
CFLAGS += -march=armv8-a             # Optimize for Raspberry Pi 4 (ARMv8)
CFLAGS += -DNDEBUG					# Disable assert() macro
CFLAGS += -DEI_CLASSIFIER_ENABLE_DETECTION_POSTPROCESS_OP	# Add TFLite_Detection_PostProcess operation

# C++ only compiler flags
CXXFLAGS += -std=c++14				# Use C++14 standard

# Linker flags
LDFLAGS += -lm 						# Link to math.h
LDFLAGS += -lstdc++					# Link to stdc++.h
LDFLAGS += -lasound                 # Link to ALSA (audio capture library)
LDFLAGS += $(shell python3-config --ldflags)  # Link Python library
LDFLAGS += -L/usr/lib/python3.11/config-3.11-aarch64-linux-gnu -lpython3.11 # Pham Tien Dat add

# Include C source code for required libraries
CSOURCES += $(wildcard edge-impulse-sdk/CMSIS/DSP/Source/TransformFunctions/*.c) \
			$(wildcard edge-impulse-sdk/CMSIS/DSP/Source/CommonTables/*.c) \
			$(wildcard edge-impulse-sdk/CMSIS/DSP/Source/BasicMathFunctions/*.c) \
			$(wildcard edge-impulse-sdk/CMSIS/DSP/Source/ComplexMathFunctions/*.c) \
			$(wildcard edge-impulse-sdk/CMSIS/DSP/Source/FastMathFunctions/*.c) \
			$(wildcard edge-impulse-sdk/CMSIS/DSP/Source/SupportFunctions/*.c) \
			$(wildcard edge-impulse-sdk/CMSIS/DSP/Source/MatrixFunctions/*.c) \
			$(wildcard edge-impulse-sdk/CMSIS/DSP/Source/StatisticsFunctions/*.c)

# Include C++ source code for required libraries
CXXSOURCES += 	$(wildcard tflite-model/*.cpp) \
				$(wildcard edge-impulse-sdk/dsp/kissfft/*.cpp) \
				$(wildcard edge-impulse-sdk/dsp/dct/*.cpp) \
				$(wildcard edge-impulse-sdk/dsp/memory.cpp) \
				$(wildcard edge-impulse-sdk/porting/posix/*.c*) \
				$(wildcard edge-impulse-sdk/porting/mingw32/*.c*)

# Additional sources for TensorFlow Lite Micro
CSOURCES +=	edge-impulse-sdk/tensorflow/lite/c/common.c
CCSOURCES +=	$(wildcard edge-impulse-sdk/tensorflow/lite/kernels/*.cc) \
				$(wildcard edge-impulse-sdk/tensorflow/lite/kernels/internal/*.cc) \
				$(wildcard edge-impulse-sdk/tensorflow/lite/micro/kernels/*.cc) \
				$(wildcard edge-impulse-sdk/tensorflow/lite/micro/*.cc) \
				$(wildcard edge-impulse-sdk/tensorflow/lite/micro/memory_planner/*.cc) \
				$(wildcard edge-impulse-sdk/tensorflow/lite/core/api/*.cc)

# Generate names for the output object files (*.o)
COBJECTS := $(patsubst %.c,%.o,$(CSOURCES))
CXXOBJECTS := $(patsubst %.cpp,%.o,$(CXXSOURCES))
CCOBJECTS := $(patsubst %.cc,%.o,$(CCSOURCES))

# Default rule
.PHONY: all
all: app

# Compile library source code into object files
$(COBJECTS) : %.o : %.c
$(CXXOBJECTS) : %.o : %.cpp
$(CCOBJECTS) : %.o : %.cc
%.o: %.c
	$(CC) $(CFLAGS) -c $^ -o $@
%.o: %.cc
	$(CXX) $(CFLAGS) $(CXXFLAGS) -c $^ -o $@
%.o: %.cpp
	$(CXX) $(CFLAGS) $(CXXFLAGS) -c $^ -o $@

# Build target (must use C++ compiler)
.PHONY: app
app: $(COBJECTS) $(CXXOBJECTS) $(CCOBJECTS)
	mkdir -p $(BUILD_PATH)
	$(CXX) $(COBJECTS) $(CXXOBJECTS) $(CCOBJECTS) -o $(BUILD_PATH)/$(NAME) $(LDFLAGS)

# Remove compiled object files
.PHONY: clean
clean:
	rm -f $(COBJECTS)
	rm -f $(CCOBJECTS)
	rm -f $(CXXOBJECTS)
