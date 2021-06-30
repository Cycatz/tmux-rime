CXX = gcc
CXXFLAGS = -fPIC -shared -Wall -Wextra -Wstrict-prototypes -O2 -std=c11
LDLIBS += -lrime

SRC_EXT := c
SOURCE := rime.$(SRC_EXT) 
TARGET := libwrime.so

.PHONY = clean

all: $(TARGET)

$(TARGET): $(SOURCE) 
	@echo "$(CXX) $(CXXFLAGS) $(LDLIBS) $< -o $@"; $(CXX) $(CXXFLAGS) $(LDLIBS) $< -o $@
clean:
	@echo "$(RM) $(TARGET)"; $(RM) $(TARGET)
