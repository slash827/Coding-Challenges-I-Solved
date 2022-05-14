#include <string>
#include <list>
#include <utility>
#include "PostMessage.h"
using namespace std;
class USocial;

class User
{
    friend class USocial;

private:
     bool isFriend(unsigned long id);
protected:
    USocial *us;
    unsigned long id = 0; // id=0 is not valid, it means that it's not initialized yet
    string name;
    list<unsigned long> friends{}; // id is the friend's key
    list<Post *> posts;
    list<Message *> receivedMsgs;
    User(USocial *us, string name);
    ~User();
public:
    unsigned long getId();
    string getName();
    void addFriend(User *user);
    void removeFriend(User *user);
    void post(const string& text);
    void post(const string& text, Media *media);
    list<Post*> getPosts();
    void viewFriendsPosts();
    void receiveMessage(Message *message);
    virtual void sendMessage(User *user, Message *message);
    void viewReceivedMessages();
};

class BusinessUser: public User
{
public:
    ~BusinessUser() = default;
    void sendMessage(User *user, Message *message) override;
    BusinessUser(USocial *us, string name) :
            User(us, std::move(name))
    {}
};