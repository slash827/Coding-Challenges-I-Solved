class Media
{
public:
    Media();
    virtual void display();
};

class Photo: public Media
{
public:
    void display() override;
};

class Audio: public Media
{
public:
    void display() override;
};

class Video: public Media
{
public:
    void display() override;
};
