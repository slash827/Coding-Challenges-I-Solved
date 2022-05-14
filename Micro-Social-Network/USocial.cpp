#include <list>
#include <string>
#include <map>
#include <utility>
#include "exceptions.h"
#include "USocial.h"

using namespace std;

USocial::~USocial()
{
    // should delete all the users in the network
    for(auto & user : this->users)
        delete user.second;
}
User* USocial::registerUser(string name, bool isBusiness)
{
    User* newUser;
    if(isBusiness) // in case it's a business user
        newUser = new BusinessUser(this, std::move(name));
    else
        newUser = new User(this, name);

    // here assign the next id available for the user
    newUser->id = this->next_id;
    this->next_id++;
    this->users.insert(pair(newUser->id, newUser));

    return newUser;
}
void USocial::removeUser(User *user)
{
    bool isFound = false; // variable to check if the user was found
    for (auto it = this->users.begin(); it != this->users.end(); ++it)
        if (it->second->getId() == user->getId()) {
            // deletes it from the list of users
            this->users.erase(it);
            isFound = true;
            break;
        }
    if(!isFound) {
        // in case the user is not in the network
        try { throw UsException("The user you wish to remove was not found"); }
        catch (exception &e) {e.what(); }
    }
}
User* USocial::getUserById(unsigned long id)
{
    map<unsigned long, User*>::iterator it;
    it = this->users.find(id); // iterator to find the given id inside the list
    if (it != this->users.end())
        return it->second;
    else {
        // in case such id does not belong to any user in the network
        try { throw UsException("There is no user with specified id"); }
        catch (exception &e) {
            e.what();
            return nullptr;
        }
    }
}