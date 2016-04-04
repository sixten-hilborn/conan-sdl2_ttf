from conans import ConanFile
from conans.tools import download, unzip, replace_in_file
import os
import shutil
from conans import CMake, ConfigureEnvironment
import platform

class SDL2TTfConan(ConanFile):
    name = "SDL2_ttf"
    version = "2.0.14"
    folder = "SDL2_ttf-%s" % version
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = '''shared=False
    fPIC=True'''
    generators = "cmake"
    url="http://github.com/lasote/conan-SDL2_ttf"
    requires = "SDL2/2.0.4@lasote/stable", "freetype/2.6.3@lasote/stable"
    license="MIT"

    def config(self):
        del self.settings.compiler.libcxx 

    def source(self):
        zip_name = "%s.tar.gz" % self.folder
        download("https://www.libsdl.org/projects/SDL_ttf/release/%s" % zip_name, zip_name)
        unzip(zip_name)

    def build(self):
        if self.settings.os == "Windows":
            self.output.error("Windows not supported yet. Contact the author on github: github.com/lasote/conan-SDL2_ttf")
        else:
            self.build_with_make()

   
    def build_with_make(self):
        
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        if self.options.fPIC:
            env_line = env.command_line.replace('CFLAGS="', 'CFLAGS="-fPIC ')
        else:
            env_line = env.command_line
        
        print(self.deps_cpp_info)
        # env_line = env_line.replace('LIBS="', 'LIBS2="') # Rare error if LIBS is kept
        sdl2_config_path = os.path.join(self.deps_cpp_info["SDL2"].lib_paths[0], "sdl2-config")
        self.run("cd %s" % self.folder)
        self.run("chmod a+x %s/configure" % self.folder)
        self.run("chmod a+x %s" % sdl2_config_path)
        
        self.output.warn(env_line)
        if self.settings.os == "Macos": # Fix rpath, we want empty rpaths, just pointing to lib file
            old_str = "-install_name \$rpath/"
            new_str = "-install_name "
            replace_in_file("%s/configure" % self.folder, old_str, new_str)
        
        freetype_location = self.deps_cpp_info["freetype"].lib_paths[0]       
        shared = "--enable-shared=yes --enable-static=no" if self.options.shared else "--enable-shared=no --enable-static=yes"
        configure_command = 'cd %s && %s SDL2_CONFIG=%s ./configure --with-freetype-exec-prefix="%s" %s' % (self.folder, env_line, sdl2_config_path, freetype_location, shared)
        self.output.warn("Configure with: %s" % configure_command)
        self.run(configure_command)
        
        
        old_str = '\nLIBS = '
        new_str = '\n# Removed by conan: LIBS2 = '
        replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
        
        old_str = '\nLIBTOOL = '
        new_str = '\nLIBS = %s \nLIBTOOL = ' % " ".join(["-l%s" % lib for lib in self.deps_cpp_info.libs]) # Trust conaaaan!
        replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
       
        old_str = '\nSDL_CFLAGS ='
        new_str = '\n# Commented by conan: SDL_CFLAGS ='
        replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
        
        old_str = '\nSDL_LIBS ='
        new_str = '\n# Commented by conan: SDL_LIBS ='
        replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
        
        old_str = '\nCFLAGS ='
        new_str = '\n# Commented by conan: CFLAGS ='
        replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
        
        old_str = '\n# Commented by conan: CFLAGS ='
        fpic = "-fPIC"  if self.options.fPIC else ""
        m32 = "-m32" if self.settings.arch == "x86" else ""
        debug = "-g" if self.settings.build_type == "Debug" else "-s -DNDEBUG"
        new_str = '\nCFLAGS =%s %s %s %s\n# Commented by conan: CFLAGS =' % (" ".join(self.deps_cpp_info.cflags), fpic, m32, debug)
        replace_in_file("%s/Makefile" % self.folder, old_str, new_str)
        
        
        self.output.warn(str(self.deps_cpp_info.libs))
        
        self.run("cd %s && %s make" % (self.folder, env_line))
        
    def package(self):
        """ Define your conan structure: headers, libs and data. After building your
            project, this method is called to create a defined structure:
        """
        self.copy(pattern="SDL_ttf.h", dst="include", src="%s" % self.folder, keep_path=False)
        self.copy(pattern="SDL_ttf.h", dst="include/SDL2", src="%s" % self.folder, keep_path=False)
        
        # UNIX
        if not self.options.shared:
            self.copy(pattern="*.a", dst="lib", src="%s" % self.folder, keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="%s" % self.folder, keep_path=False)   
        else:
            self.copy(pattern="*.so*", dst="lib", src="%s" % self.folder, keep_path=False)
            self.copy(pattern="*.dylib*", dst="lib", src="%s" % self.folder, keep_path=False)

    def package_info(self):  
                
        self.cpp_info.libs = ["SDL2_ttf"]
