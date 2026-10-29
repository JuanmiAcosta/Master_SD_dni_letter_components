cmake_minimum_required(VERSION 3.16)

project(dni_utils
    VERSION 1.0.0
    DESCRIPTION "Librería C++ para calcular y validar el DNI español"
    LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Por defecto se genera una librería compartida (.so); con
# -DBUILD_SHARED_LIBS=OFF se genera una estática (.a).
option(BUILD_SHARED_LIBS "Compilar dni_utils como librería compartida" ON)

# --- Librería -----------------------------------------------------------------
add_library(dni_utils src/dni_utils.cpp)
target_include_directories(dni_utils PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)
target_compile_options(dni_utils PRIVATE -Wall -Wextra -Wpedantic)
set_target_properties(dni_utils PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
    PUBLIC_HEADER src/dni_utils.h)

# --- Cliente ------------------------------------------------------------------
add_executable(prueba client/prueba.cpp)
target_link_libraries(prueba PRIVATE dni_utils)
target_compile_options(prueba PRIVATE -Wall -Wextra -Wpedantic)

# --- Instalación (cmake --install build --prefix <dir>) -----------------------
include(GNUInstallDirs)
install(TARGETS dni_utils prueba
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

# --- Documentación (cmake --build build --target docs) ------------------------
find_package(Doxygen)
if(DOXYGEN_FOUND)
    add_custom_target(docs
        COMMAND ${DOXYGEN_EXECUTABLE} Doxyfile
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/docs
        COMMENT "Generando documentación con Doxygen en docs/html"
        VERBATIM)
endif()
