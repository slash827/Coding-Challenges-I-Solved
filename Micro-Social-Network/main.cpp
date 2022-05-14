#include <exception>
#include <iostream>
#include "USocial.h"
#include "Media.h"

// that's the main that tests the implementation of the social network
int main()
{
    USocial us;
    User* u1 = us.registerUser("Liron");
    User* u2 = us.registerUser("Yahav");
    User* u3 = us.registerUser("Shachaf");
    User* u4 = us.registerUser("Tsur", true);
    User* u5 = us.registerUser("Elit");
    u1->post("Hello world!");
    u2->post("I'm having a great time here :)", new Audio());
    u3->post("This is awesome!", new Photo());
    u5->addFriend(u1);
    u5->addFriend(u2);
    u5->viewFriendsPosts(); // should see only u1, u2 s' posts
    u4->sendMessage(u5, new Message("Buy Falafel!"));
    u5->viewReceivedMessages();
    try {
        u3->sendMessage(u5, new Message("All your base are belong to us"));
    }
    catch (exception &e) {
        cout << "error: " << e.what() << endl;
    }
    u5->viewReceivedMessages();
    u3->addFriend(u5);
    u3->sendMessage(u5, new Message("All your base are belong to us"));
    u5->viewReceivedMessages();
    return 0;
}