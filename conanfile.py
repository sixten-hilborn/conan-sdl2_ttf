#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class Sdl2TtfConan(ConanFile):
    name = "sdl2_ttf"
    version = "2.0.14"
    url = "http://github.com/sixten-hilborn/conan-sdl2_ttf"
    description = "Library to load and use TrueType fonts"
    
    # Indicates License type of the packaged library
    license = "zlib"
    
    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]
    
    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake" 
    
    # Options may need to change depending on the packaged library. 
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = (
        'shared=False',
        'fPIC=True'
    )
    
    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    
    # Use version ranges for dependencies unless there's a reason not to
    requires = (
        "sdl2/[>=2.0.4]@bincrafters/stable",
    )

    def requirements(self):
        #if self.settings.os != "Windows":
        self.requires("freetype/[>=2.8.1]@bincrafters/stable")

    def configure(self):
        if self.settings.os == "Windows":
            self.options.fPIC = False
        del self.settings.compiler.libcxx
        #self.options["SDL2"].shared = self.options.shared

    def source(self):
        extracted_dir = "SDL2_ttf-" + self.version
        source_url = "https://www.libsdl.org/projects/SDL_ttf"
        tools.get("{0}/release/{1}.tar.gz".format(source_url, extracted_dir))

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

        
    def build(self):
        #if self.settings.os == "Windows":
        #    pass
        #else:
        #    self.build_with_make()
        self.build_cmake()

    def build_cmake(self):
        shutil.copy("CMakeLists.txt", "%s/CMakeLists.txt" % self.source_subfolder)
        cmake = CMake(self)
        cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.configure(build_folder=self.build_subfolder, source_folder=self.source_subfolder)
        cmake.build()
        #cmake.install()


    #def build_with_make(self):
    #
    #    env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
    #    if self.options.fPIC:
    #        env_line = env.command_line.replace('CFLAGS="', 'CFLAGS="-fPIC ')
    #    else:
    #        env_line = env.command_line
    #
    #    # env_line = env_line.replace('LIBS="', 'LIBS2="') # Rare error if LIBS is kept
    #    sdl2_config_path = os.path.join(self.deps_cpp_info["SDL2"].lib_paths[0], "sdl2-config")
    #    self.run("cd %s" % self.folder)
    #    self.run("chmod a+x %s/configure" % self.folder)
    #    self.run("chmod a+x %s" % sdl2_config_path)
    #
    #    self.output.warn(env_line)
    #    if self.settings.os == "Macos": # Fix rpath, we want empty rpaths, just pointing to lib file
    #        old_str = "-install_name \$rpath/"
    #        new_str = "-install_name "
    #        tools.replace_in_file("%s/configure" % self.folder, old_str, new_str)
    #    if self.settings.os == "Linux":
    #        env_line = env_line.replace("-lbz2", "") # Configure fails because of double main declaration WTF
    #
    #    freetype_location = self.deps_cpp_info["freetype"].lib_paths[0]
    #    shared = "--enable-shared=yes --enable-static=no" if self.options.shared else "--enable-shared=no --enable-static=yes"
    #    configure_command = 'cd %s && %s SDL2_CONFIG=%s ./configure --with-freetype-exec-prefix="%s" %s' % (self.folder, env_line, sdl2_config_path, freetype_location, shared)
    #    self.output.warn("Configure with: %s" % configure_command)
    #    self.run(configure_command)
    #
    #
    #    old_str = '\nLIBS = '
    #    new_str = '\n# Removed by conan: LIBS2 = '
    #    tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
    #
    #    old_str = '\nLIBTOOL = '
    #    new_str = '\nLIBS = %s \nLIBTOOL = ' % " ".join(["-l%s" % lib for lib in self.deps_cpp_info.libs]) # Trust conaaaan!
    #    tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
    #
    #    old_str = '\nSDL_CFLAGS ='
    #    new_str = '\n# Commented by conan: SDL_CFLAGS ='
    #    tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
    #
    #    old_str = '\nSDL_LIBS ='
    #    new_str = '\n# Commented by conan: SDL_LIBS ='
    #    tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
    #
    #    old_str = '\nCFLAGS ='
    #    new_str = '\n# Commented by conan: CFLAGS ='
    #    tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
    #
    #    old_str = '\n# Commented by conan: CFLAGS ='
    #    fpic = "-fPIC"  if self.options.fPIC else ""
    #    m32 = "-m32" if self.settings.arch == "x86" else ""
    #    debug = "-g" if self.settings.build_type == "Debug" else "-s -DNDEBUG"
    #    new_str = '\nCFLAGS =%s %s %s %s\n# Commented by conan: CFLAGS =' % (" ".join(self.deps_cpp_info.cflags), fpic, m32, debug)
    #    tools.replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
    #
    #
    #    self.output.warn(str(self.deps_cpp_info.libs))
    #
    #    self.run("cd %s && %s make" % (self.folder, env_line))


    def package(self):
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can replace all the steps below with the word "pass"
        self.copy(pattern="LICENSE")
        self.copy(pattern="*SDL_ttf.h", dst="include/SDL2", src=self.source_subfolder)
        self.copy(pattern="*.dll", dst="bin", src=self.build_subfolder, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy(pattern="*.a", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy(pattern="*.so", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy(pattern="*.so.*", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src=self.build_subfolder, keep_path=False)
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs.append('include/SDL2')
