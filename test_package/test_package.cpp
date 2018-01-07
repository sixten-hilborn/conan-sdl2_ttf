#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>

#include <iostream>

int main(int argv, char* argc[])
{
	const char fontName[] = "OpenSans-Bold.ttf";

	if ( SDL_Init( SDL_INIT_EVERYTHING ) == -1 )
	{
		std::cout << " Failed to initialize SDL : " << SDL_GetError() << std::endl;
		return 1;
	}

	if ( TTF_Init() == -1 )
	{
		std::cout << " Failed to initialize TTF : " << SDL_GetError() << std::endl;
		return 1;
	}

	// Load our fonts, with a huge size
	TTF_Font* font = TTF_OpenFont(fontName, 90);
	if (!font)
	{
		std::cout << "Could not load font " << fontName;
		return 1;
	}

	TTF_Quit();
	SDL_Quit();

	return 0;
}
