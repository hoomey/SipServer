#pragma once
#ifndef SIPSERVER_AUTHMANAGER_HPP
#define SIPSERVER_AUTHMANAGER_HPP

#include <chrono>

#include <resip/stack/Helper.hxx>
#include <rutil/Data.hxx>


using namespace std::chrono_literals;

class Nonce {
    private:
        resip::Data mValue;
        std::chrono::steady_clock::time_point mCreated;
        const std::chrono::steady_clock::duration mTimeout = 1min;

    private:
        void generateNonce();

    public:
        Nonce();
        resip::Data getValue();
};

class AuthManager {
    public:
        void addAuthParameters(resip::SipMessage& msg);
        bool isAuth(resip::SipMessage& msg);

    private:
        Nonce nonce;
};




#endif //SIPSERVER_AUTHMANAGER_HPP
