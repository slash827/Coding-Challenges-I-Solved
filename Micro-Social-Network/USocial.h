#include "User.h"
#include <map>

using namespace std;
class User;

class USocial
{
private:
    map<unsigned long, User*> users;
    unsigned long next_id = 1;
public:
    USocial() = default;
    ~USocial();
    User* registerUser(string name, bool isBusiness=false);
    void removeUser(User *user);
    User* getUserById(unsigned long id);
};