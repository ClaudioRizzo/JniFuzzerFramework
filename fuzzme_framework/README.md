# Build the Project

```bash
cd build; # create it before if you do not have the folder

# Set BUILD_TESTS to OFF or do not include it if you do not want to build tests
cmake -DCMAKE_CXX_COMPILER=/home/clod/android-toolchain-arm-api-23/bin/clang++ -DBUILD_TESTS=ON ..
make
```
