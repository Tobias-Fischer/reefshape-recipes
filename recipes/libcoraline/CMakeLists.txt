# Coraline (TagLab's "Refine border" graph-cut) as a shared library, loaded from Python with ctypes.
# The upstream CMakeLists.txt passes `-c` to the linker and pins flags; this is the minimum.
cmake_minimum_required(VERSION 3.15)
project(coraline LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN ON)
if(MSVC)
  add_compile_definitions(_CRT_SECURE_NO_DEPRECATE)
endif()
# maxflow (Boykov-Kolmogorov) is vendored in src/maxflow and instantiated in coraline.cpp
add_library(coraline SHARED src/coraline.cpp src/mutualedges.cpp src/coralinepy.cpp)
target_include_directories(coraline PRIVATE src)
install(TARGETS coraline RUNTIME DESTINATION bin LIBRARY DESTINATION lib ARCHIVE DESTINATION lib)
