find_package(Threads)


find_package(Boost COMPONENTS program_options REQUIRED)
find_package(spdlog REQUIRED)

set(SOURCES
    src/main.cpp
    )

source_group(TREE ${CMAKE_CURRENT_SOURCE_DIR} FILES ${SOURCES})

add_executable(server ${SOURCES})
#target_include_directories( server PRIVATE ${Boost_INCLUDE_DIR})
target_link_libraries(server
    PRIVATE
        Boost::program_options
        spdlog::spdlog
        proto
    )
