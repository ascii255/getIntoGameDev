all: clean build open

build:
	cmake -S. -Bbuild -GXcode

clean:
	rm -rf build

open:
	sleep 2
	open build/*.xcodeproj
