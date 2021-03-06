#ifndef SIPSERVER_DB_HXX
#define SIPSERVER_DB_HXX

#include <easylogging++.h>

#include <sqlite3.h>
#include <sqlite_orm.h>

using namespace sqlite_orm;

struct User {
    size_t id;
    std::string name;
    std::string password;
};

struct Location {
    size_t id;
    std::string address;
    size_t expired;
    size_t user;
};

inline auto initStorage(const std::string& path) {
    auto storage = make_storage(path,
                                make_table("users",
                                           make_column("id",
                                                       &User::id,
                                                       autoincrement(),
                                                       primary_key()),
                                           make_column("name",
                                                       &User::name,
                                                       unique()),
                                           make_column("password",
                                                       &User::password)),
                                make_table("locations",
                                           make_column("id",
                                                       &Location::id,
                                                       autoincrement(),
                                                       primary_key()),
                                           make_column("address",
                                                       &Location::address,
                                                       unique()),
                                           make_column("expired",
                                                       &Location::expired),
                                           make_column("user",
                                                       &Location::user),
                                           foreign_key(&Location::user)
                                                   .references(&User::id)));
    return storage;
}


class Db {
    public:
        using Storage = decltype(initStorage(""));
        Storage storage;

    public:
        Db(const std::string& path):
            storage(initStorage(path)) {
            LOG(DEBUG) << "Init storage in db " << path;
            auto result = storage.sync_schema(true);
            for (auto& schema : result) {
                LOG(DEBUG) << schema.first << ": " << schema.second;
            }

            initUsers();

        }
    private:
        void initUsers() {
            try {
                storage.replace(User{0, "123", "zzzxxx123"});
            }
            catch (std::system_error& se) {
                LOG(ERROR) << se.code() << " " << se.what();
            }
        }
};


#endif //SIPSERVER_DB_HXX
