#include <exception>
#include <utility>

using namespace std;

// here I created a class in case of exceptions inside the usocial class
class UsException: public exception
{
private:
    string message;
public:
    explicit UsException(string message) {this->message = std::move(message);}
    virtual string what() { return this->message; }
};

// here I created a class in case of exceptions inside the user class
class UserException: public exception
{
private:
    string message;
public:
    UserException(string message) {this->message = std::move(message);}
    virtual string what() { return this->message; }
};