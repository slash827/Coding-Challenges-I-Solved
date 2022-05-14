#include <string>
#include <iostream>
#include <list>
#include <algorithm>
#include "USocial.h"
#include "exceptions.h"
#include "Media.h"
using namespace std;

User::User(USocial *us, string name)
{
    this->us = us;
    this->name = std::move(name);
}
User::~User()
{
    // should delete all the user's posts
    while(!this->posts.empty()) {
        delete this->posts.front();
        this->posts.pop_front();
    }
    // should delete all the user's received messages
    while(!this->receivedMsgs.empty()) {
        delete this->receivedMsgs.front();
        this->receivedMsgs.pop_front();
    }
}
unsigned long User::getId()
{
    return this->id;
}
string User::getName()
{
    return this->name;
}
bool User::isFriend(unsigned long id)
{
    // first we define the iterator then we check if there is a match
    list<unsigned long>::iterator it;
    it = find(this->friends.begin(), this->friends.end(), id);

    return !(it == this->friends.end());
}
void User::addFriend(User *user) {
    unsigned long friendId = user->getId();
    try {
        // throws an error in case the user is already a friend
        if(this->isFriend(friendId))
            throw UserException("Can't add a friend that already exists");
        else
            this->friends.push_back(friendId);
    }
    catch (exception &e) {
        e.what();
    }
}
void User::removeFriend(User *user) {
    unsigned long friendId = user->getId();
    try {
        // throws an error in case it tries to remove a user that isn't in the list
        if(!this->isFriend(friendId))
            throw UserException("Can't remove a user that isn't a friend from the friend's list");
        else
            this->friends.remove(id);
    }
    catch (exception &e){
        e.what();
    }
}
void User::post(const string& text)
{
    User::post(text, nullptr);
}
void User::post(const string& text, Media *media)
{
    try {
        // make sure the post's length is greater than 0
        if(text.empty())
            throw UserException("post length must be greater than 0");
        else {
            // if it's greater we publish the post
            Post *thisPost = new Post(text, media);
            this->posts.push_back(thisPost);
        }
    }
    catch (exception &e){
        e.what();
    }
}
list<Post*> User::getPosts()
{
    return this->posts;
}
void User::viewFriendsPosts() {
    // first we print the user's name
    cout << this->name << "'s friends posts are: " << endl;

    // now we use two for loops to print all the posts of all his friends
    for(unsigned long & it : this->friends) {
        list<Post*> currentPosts = us->getUserById(it)->getPosts();
        for(auto & currentPost : currentPosts) {
            // here we print a specific post and it's possible media
            cout << currentPost->getText() << endl;
            Media *media = currentPost->getMedia();
            if(media != nullptr)
                media->display();
        }
    }
}
void User::receiveMessage(Message *message) {
    try {
        // throws an error if an empty  message was received
        if(message == nullptr)
            throw UserException("Can't add an empty message");

        this->receivedMsgs.push_back(message);
    }
    catch (exception &e) {
        e.what();
    }
}
void User::sendMessage(User *user, Message *message)
{
    try {
        // throws an error if we try to send an empty message
        if(message->getText().empty())
            throw UserException("Can't send an empty message");

        // here we check that the recipient is his friend or else he couldn't send the message
        unsigned long userId = user->getId();
        if(!this->isFriend(userId))
            throw UserException("a non-business user Can't send a message to someone who isn't you friend");

        user->receiveMessage(message);
    }
    catch (exception &e) {
        e.what();
    }
}
void User::viewReceivedMessages()
{
    cout << this->name << "'s received messages are: " << endl;
    // here we iterate through the list of received messages
    for(auto & receivedMsg : this->receivedMsgs)
            cout << receivedMsg->getText() << endl;
}

void BusinessUser::sendMessage(User *user, Message *message)
{
    try {
        // throws an error if the message we try to send is empty
        if(message->getText().empty())
            throw UserException("Can't send an empty message");

        user->receiveMessage(message);
    }
    catch (exception &e) {
        e.what();
    }
}