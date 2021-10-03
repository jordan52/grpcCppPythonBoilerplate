find_package(Threads)

set(SOURCES
    src/main.cpp
    )

source_group(TREE ${CMAKE_CURRENT_SOURCE_DIR} FILES ${SOURCES})

add_executable(server ${SOURCES})
target_link_libraries(server
    PRIVATE
    proto
    )
