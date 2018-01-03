cmake_minimum_required(VERSION 2.8.12)

# Project Name and start working in project scope (some things just work until now, some just work after this command)
project(SDL2_ttf C)

# Add conan dependencies
include(../conanbuildinfo.cmake)
conan_basic_setup()

set(SOURCE_FILES
  SDL_ttf.c)

add_library(SDL2_ttf ${SOURCE_FILES})
target_link_libraries(SDL2_ttf ${CONAN_LIBS})
