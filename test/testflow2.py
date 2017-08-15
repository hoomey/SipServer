import socket
import subprocess
import time
import platform
import logging
import re

from config import Config
from utils import timeout, printName, handleLogDir, printConsoleOut

config = Config()

address = config.address
port = config.port
path = config.path
interface = config.interface
serverEndPoint = config.serverEndPoint

TIMEOUT_LIMIT = 5
TEST_MESSAGES = ['Hello', 'World', 'q']
ERROR_MSG_PATTERN = re.compile(R"Exit with error code (?P<errorCode>\d+)")


def process(command, multiConnection=False):
    result = []
    commandResult = subprocess.Popen(command)
    result.append(commandResult)

    if not multiConnection:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        result.append(clientSocket)
    else:
        amountClients = 3
        sockets = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(amountClients)]
        result.append(sockets)

    time.sleep(0.1)
    return tuple(result)


@handleLogDir
@printName
@timeout(TIMEOUT_LIMIT)
def inMessageInLog():
    result, clientSocket = process([path, '-p', port, '-l', 'INFO'])

    for m in TEST_MESSAGES:
        logging.debug(f'< {m}')
        clientSocket.sendto(m.encode(), serverEndPoint)

    logFile = open('./logs/myeasylog.log')

    reason = None
    if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
        for line in logFile:
            logging.debug(f'log: {line[:-1]}')

    logFile.seek(0)
    isAllMessagedLogged = all(any(line.find(x) != -1 for line in logFile) for x in TEST_MESSAGES)
    if not isAllMessagedLogged:
        reason = 'Not all input messaged are logged'
    return isAllMessagedLogged, reason


@handleLogDir
@printName
@timeout(TIMEOUT_LIMIT)
def outMessageInLog():
    result, clientSocket = process([path, '-p', port, '-l', 'INFO'])

    for m in TEST_MESSAGES:
        logging.debug(f'< {m}')
        clientSocket.sendto(m.encode(), serverEndPoint)

    logFile = open('./logs/myeasylog.log')

    reason = None
    if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
        for line in logFile:
            logging.debug(f'log: {line[:-1]}')

    logFile.seek(0)
    isAllMessagedLogged = all(any(line.find(x) != -1 for line in logFile) for x in TEST_MESSAGES)
    if not isAllMessagedLogged:
        reason = 'Not all output messaged are logged'
    return isAllMessagedLogged, reason


@handleLogDir
@printName
@timeout(TIMEOUT_LIMIT)
def usedPortInLog():
    usedSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    usedSocket.sendto("q".encode(), serverEndPoint)
    usedPort = usedSocket.getsockname()[-1]

    result, clientSocket = process([path, '-p', str(usedPort), '-l', 'DEBUG'])
    for m in TEST_MESSAGES:
        logging.debug(f'< {m}')
        clientSocket.sendto(m.encode(), serverEndPoint)

    logFile = open('./logs/myeasylog.log')

    reason = None
    if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
        for line in logFile:
            logging.debug(f'log: {line[:-1]}')

    logFile.seek(0)
    fileText = logFile.read()
    matches = re.findall(ERROR_MSG_PATTERN,fileText)
    print(matches)
    if not matches:
        reason = 'There are messages about error code in log'
        return False, reason
    CORRECT_CODE = 1
    RETURN_CODE = matches[0]
    isReturnCodeCorrect = RETURN_CODE == CORRECT_CODE
    if not isReturnCodeCorrect:
        reason = f"Error code is incorrect. Must be {CORRECT_CODE}, now {matches[0]}"
    return isReturnCodeCorrect, reason

@handleLogDir
@printName
@timeout(TIMEOUT_LIMIT)
def unavailablePortInLog():
    osType = platform.system()
    logging.debug(f'OS is  {osType}')
    if osType != 'Linux':
        return True
    result, _ = process([path, '-p', '54'])
    logFile = open('./logs/myeasylog.log')

    reason = None
    if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
        for line in logFile:
            logging.debug(f'log: {line[:-1]}')

    logFile.seek(0)
    fileText = logFile.read()
    matches = re.findall(ERROR_MSG_PATTERN,fileText)
    print(matches)
    if not matches:
        reason = 'There are messages about error code in log'
        return False, reason
    CORRECT_CODE = 2
    RETURN_CODE = matches[0]
    isReturnCodeCorrect = RETURN_CODE == CORRECT_CODE
    if not isReturnCodeCorrect:
        reason = f"Error code is incorrect. Must be {CORRECT_CODE}, now {mathes[0]}"
    return isReturnCodeCorrect, reason


@handleLogDir
@printName
@timeout(TIMEOUT_LIMIT)
def unavailableInterfaceLog():
    usedSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    usedSocket.sendto("q".encode(), serverEndPoint)
    usedPort = usedSocket.getsockname()[-1]

    result, clientSocket = process([path, '-p', str(usedPort), '-l', 'DEBUG'])
    for m in TEST_MESSAGES:
        logging.debug(f'< {m}')
        clientSocket.sendto(m.encode(), serverEndPoint)

    logFile = open('./logs/myeasylog.log')

    reason = None
    if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
        for line in logFile:
            logging.debug(f'log: {line[:-1]}')

    logFile.seek(0)
    fileText = logFile.read()
    matches = re.findall(ERROR_MSG_PATTERN, fileText)
    print(matches)
    if not matches:
        reason = 'There are messages about error code in log'
        return False, reason
    CORRECT_CODE = 3
    RETURN_CODE = matches[0]
    isReturnCodeCorrect = RETURN_CODE == CORRECT_CODE
    if not isReturnCodeCorrect:
        reason = f"Error code is incorrect. Must be {CORRECT_CODE}, now {matches[0]}"
    return isReturnCodeCorrect, reason

#tests = [inMessageInLog, outMessageInLog]
tests = [usedPortInLog, unavailablePortInLog, unavailableInterfaceLog]