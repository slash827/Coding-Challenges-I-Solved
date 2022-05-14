#include <utility>
#include "Media.h"
#include "PostMessage.h"

// basic constructor and get method for the message object
Message::Message(string text)
{
    this->_text = std::move(text);
}
string Message::getText()
{
    return this->_text;
}

// basic constructor, dtor and get methods for the Post object
Post::Post(string text)
{
    this->_text = std::move(text);
    this->_media = nullptr;
}
Post::Post(string text, Media *media)
{
    this->_text = std::move(text);
    this->_media = media;
}
string Post::getText()
{
    return this->_text;
}
Media* Post::getMedia()
{
    return this->_media;
}
Post::~Post()
{
    delete this->_media;
}