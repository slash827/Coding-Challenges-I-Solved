#include <iostream>
#include "Media.h"

using namespace std;
// right here there is the media class and  his 4 derived classes

Media::Media() = default;
void Media::display()
{
    cout << "Media" << endl;
}

void Photo::display()
{
    cout << "Photo" << endl;
}

void Audio::display()
{
    cout << "Audio" << endl;
}

void Video::display()
{
    cout << "Video" << endl;
}
