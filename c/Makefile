CC = gcc
CFLAGS = -Wall -Wextra -g

SDL2 = `pkg-config --libs --cflags sdl2 SDL2_ttf`

TARGET = dungeon
SOURCE = main.c

.PHONY: all clean
all: $(TARGET)

$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) $(SDL2) $^ -o $@

run: $(TARGET)
	./$<

clean:
	@rm -fv $(TARGET) *.o