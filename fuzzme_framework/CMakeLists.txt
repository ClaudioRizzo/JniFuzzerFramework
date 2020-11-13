cmake_minimum_required(VERSION 3.9)

project(cloddie VERSION 1.0.1 DESCRIPTION "JNI Fuzzme Framework")

option(DEBUG "Whether debug mode is on or off" OFF)
add_definitions(-std=c++11)

if(DEBUG)
    add_definitions(-std=c++11 -DDEBUG=DEBUG)
endif(DEBUG)

if(VERBOSE)
    add_definitions(-std=c++11 -DVERBOSE=VERBOSE)
endif(VERBOSE)

set(SRC_DIR "${PROJECT_SOURCE_DIR}/src")
set(INCLUDE_DIR "${PROJECT_SOURCE_DIR}/include")


set(CLANG_ANDROID_FLAGS "-fPIE -fPIC")
set(LINKER_FLAGS "-pie -static-libstdc++")
set(CMAKE_CXX_FLAGS  "${CLANG_ANDROID_FLAGS}")
set(CMAKE_EXE_LINKER_FLAGS  ${LINKER_FLAGS})

set(CMAKE_SYSTEM_NAME Android)

option(BUILD_TEST "Download or updates google test framework and builds unit tests" OFF)

if(BUILD_TESTS)
    add_subdirectory(tests)
endif(BUILD_TESTS)

add_executable(fuzz_me "")

target_include_directories(fuzz_me PRIVATE "${INCLUDE_DIR}"
                                          "${INCLUDE_DIR}/extractor"
                                          "${INCLUDE_DIR}/lib_utils"
                                          "${INCLUDE_DIR}/signature_parser"
                                          "${INCLUDE_DIR}/signature_parser/soot_parser"
                                          "${INCLUDE_DIR}/mocks"
                                          "${INCLUDE_DIR}/mocks/type_mocks"
                                          "${INCLUDE_DIR}/executor"
                                          "${INCLUDE_DIR}/executor/plugins")



target_sources(fuzz_me PUBLIC "${SRC_DIR}/extractor/jni_extractor.cpp"
                             "${SRC_DIR}/extractor/jni_dynamic_extractor.cpp"
                             "${SRC_DIR}/extractor/jni_static_extractor.cpp"
                             "${SRC_DIR}/libutils/libutils.cpp"
                             "${SRC_DIR}/signature_parser/soot_parser/soot_lexer.cpp"
                             "${SRC_DIR}/signature_parser/soot_parser/soot_parser.cpp"
                             "${SRC_DIR}/mocks/type_mocks/jstring_mock.cpp"
                             "${SRC_DIR}/mocks/type_mocks/type_mocks_utils.cpp"
                             "${SRC_DIR}/mocks/jnienv_mocks.cpp"
                             "${SRC_DIR}/mocks/function_ptr.cpp"
                             "${SRC_DIR}/mocks/jvm_mocks.cpp"
                             "${SRC_DIR}/fuzzer.cpp"
                             "${SRC_DIR}/executor/executor.cpp"
                             "${SRC_DIR}/executor/plugins/simple_executor.cpp"
                             "${SRC_DIR}/main.cpp")