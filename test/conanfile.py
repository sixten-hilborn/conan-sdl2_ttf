from conans import ConanFile, CMake
import os
from StringIO import StringIO

class DefaultNameConan(ConanFile):
    name = "DefaultName"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    generators = ["cmake"] # Generates conanbuildinfo.gcc with all deps information

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")
        self.copy(pattern="*.ttf", dst="bin", src="")

    def test(self):
        out = StringIO()
        self.run("cd bin && .%sexample || true" % (os.sep),  output=out)
        print("**********\n%s***********" % str(out.getvalue()))
        assert "Couldn't find matching render driver" in str(out.getvalue()) or "No available video device" in str(out.getvalue()) or "Closing window" in str(out.getvalue())
        
