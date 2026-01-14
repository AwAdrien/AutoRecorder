Net::Socket@ sock = null;
Net::Socket@ clientSock = null;

const uint16 PORT = 8477;

bool recording = false;

void OnRunStep(SimulationManager@ sim) {
     if (@clientSock is null) {
        return;
    }

    int time = sim.RaceTime;

    if (time == -2000) {
        clientSock.Write(1);
        recording = true;
    }

    TM::PlayerInfo@ player = sim.PlayerInfo;
    if (recording && @player != null && player.RaceFinished) {
        clientSock.Write(0);
        TM::GameCtnChallenge@ challenge = GetCurrentChallenge();
        if (@challenge != null) {
            clientSock.Write(challenge.Name.Length);
            clientSock.Write(challenge.Name);
        }
        recording = false;
    }
}



void Main()
{
    if (@sock is null) {
        @sock = Net::Socket();
        sock.Listen("127.0.0.1", PORT);
    }
}

void Render()
{
    auto @newSock = sock.Accept(0);
    if (@newSock !is null) {
        @clientSock = @newSock;
        log("Client connected (IP: " + clientSock.RemoteIP + ")");
    }
}

PluginInfo@ GetPluginInfo()
{
    auto info = PluginInfo();
    info.Name = "Autorecord";
    info.Author = "Adrien";
    info.Version = "v0.0.0";
    info.Description = "Auto records run !!";
    return info;
}