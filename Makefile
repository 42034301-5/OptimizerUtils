CXXFLAGS   = -std=c++17
CXX        = g++
RM         = rm -f
OBJ        = tri2quad quad2tri split
SOURCE     = tri2quad.cpp quad2tri.cpp split.cpp

build : $(OBJ)
	echo DONE!

%.exe:%.cpp
	$(CXX) -o $@ $<

.PHONY : clean
clean:
	$(RM) *.bak $(OBJ)
	touch *.*
