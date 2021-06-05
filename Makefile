CXX = gcc
CXXFLAGS = -Wall -g -fno-diagnostics-color 
LDLIBS += -lrime

SRC_EXT := c
SOURCE := rime.c 
TARGET := rime 

.PHONY = clean

all: $(TARGET)

$(TARGET): $(SOURCE) 
	@echo "$(CXX) $(CXXFLAGS) $(LDLIBS) $< -o $@"; $(CXX) $(CXXFLAGS) $(LDLIBS) $< -o $@
clean:
	@echo "$(RM) $(TARGET)"; $(RM) $(TARGET)

