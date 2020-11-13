# Download and unpack googletest at configure time
configure_file(CMakeLists.txt.in googletest-download/CMakeLists.txt)

set(TEST_BUILD_FOLDER ${CMAKE_BINARY_DIR}/tests)
set(TEST_SRC ${PROJECT_SOURCE_DIR}/tests)
# set(INCLUDE_DIR "${PROJECT_SOURCE_DIR}/include")

execute_process(COMMAND "${CMAKE_COMMAND}" -G "${CMAKE_GENERATOR}" .
    WORKING_DIRECTORY "${TEST_BUILD_FOLDER}/googletest-download" )
execute_process(COMMAND "${CMAKE_COMMAND}" --build .
    WORKING_DIRECTORY "${TEST_BUILD_FOLDER}/googletest-download" )

# Prevent GoogleTest from overriding our compiler/linker options
# when building with Visual Studio
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

# Add googletest directly to our build. This adds
# the following targets: gtest, gtest_main, gmock
# and gmock_main
add_subdirectory("${CMAKE_BINARY_DIR}/googletest-src"
                "${CMAKE_BINARY_DIR}/googletest-build")

# including gtest directory
enable_testing()
include_directories("${gtest_SOURCE_DIR}/include"
                    "${gmock_SOURCE_DIR}/include")


add_executable(unit_tests "")
# Link test executable against gtest & gtest_main
target_link_libraries(unit_tests gtest gtest_main)
add_test( unit_tests unit_tests )

target_include_directories(unit_tests PRIVATE "${INCLUDE_DIR}" 
                                        "${INCLUDE_DIR}/libutils"
                                        "${INCLUDE_DIR}/mocks"
                                        "${INCLUDE_DIR}/mocks/type_mocks"
                                        "${INCLUDE_DIR}/signature_parser"
                                        "${INCLUDE_DIR}/signature_parser/soot_parser"
                                        "${gtest_SOURCE_DIR}/include")

target_sources(unit_tests PUBLIC "${TEST_SRC}/test_main.cpp" 
                                 "${TEST_SRC}/test_libutils.cpp"
                                 "${SRC_DIR}/libutils/libutils.cpp"
                                 "${TEST_SRC}/test_dynamic_extractor.cpp"
                                 "${TEST_SRC}/test_extractor.cpp"
                                 "${SRC_DIR}/extractor/jni_dynamic_extractor.cpp"
                                 "${SRC_DIR}/extractor/jni_extractor.cpp"
                                 "${SRC_DIR}/mocks/jnienv_mocks.cpp"
                                 "${SRC_DIR}/mocks/jvm_mocks.cpp"
                                 "${SRC_DIR}/mocks/type_mocks/jstring_mock.cpp"
                                 "${SRC_DIR}/mocks/type_mocks/type_mocks_utils.cpp"
                                 "${SRC_DIR}/signature_parser/soot_parser/soot_lexer.cpp"
                                 "${TEST_SRC}/signature_parser/test_soot_parser.cpp"
                                 "${SRC_DIR}/signature_parser/soot_parser/soot_parser.cpp")

add_custom_command(TARGET unit_tests POST_BUILD 
    COMMAND ${CMAKE_COMMAND} -E copy_directory 
        ${CMAKE_SOURCE_DIR}/tests/libutils_test_files $<TARGET_FILE_DIR:unit_tests>/libutils_test_files)

add_custom_command(TARGET unit_tests POST_BUILD 
        COMMAND ${CMAKE_COMMAND} -E copy_directory 
            ${CMAKE_SOURCE_DIR}/tests/extractor_test_files $<TARGET_FILE_DIR:unit_tests>/extractor_test_files)

add_custom_command(TARGET unit_tests POST_BUILD 
        COMMAND ${CMAKE_COMMAND} -E copy_directory 
            ${CMAKE_SOURCE_DIR}/tests/soot_parser_test_files $<TARGET_FILE_DIR:unit_tests>/soot_parser_test_files)
