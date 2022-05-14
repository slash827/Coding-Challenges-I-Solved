#include <iostream>
#include <string>
using namespace std;
class Media;

class Message
{
private:
    string _text;
public:
    explicit Message(string text);
    string getText();
};

class Post
{
private:
    string _text;
    Media *_media;
public:
    ~Post();
    explicit Post(string);
    Post(string, Media*);
    string getText();
    Media* getMedia();
};