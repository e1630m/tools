<#
    Default path of this file:
        (For Current User, Current Host) %UserProfile%/Documents/PowerShell/Microsoft.PowerShell_profile.ps1
        (For Current User, All Hosts) %UserProfile%/Documents/PowerShell/profile.ps1
        (For All Users, Current Host) $PSHOME/Microsoft.PowerShell_profile.ps1
        (For All Users, All Hosts) $PSHOME/profile.ps1
        (For POSIX) 
            %UserProfile%/Documents/PowerShell -> ~/.config/powershell
            %PSHOME -> /usr/local/microsoft/powershell/7
    
    Find and Replace:
        PAT: ghp_personal_access_tokens_of_your_GitHub_account (need repo access)
        GitHub Username: e1630m
        /path/to/the/home/directory/of/your/repos: ~/git
#>

Set-PoshPrompt agnoster
Function gcreate {
    $PAT = 'ghp_personal_access_tokens_of_your_GitHub_account'
    $REPO = '{"name":"' + $args[0] + '"}'
    curl -u e1630m:$PAT https://api.github.com/user/repos -d $REPO
}

Function gclone {
    cd ~/git
    $REPO = $args[0]
    git clone git@github.com:e1630m/$REPO
    cd $REPO
    git branch -M main
}

Function gpub {
    $PAT = 'ghp_personal_access_tokens_of_your_GitHub_account'
    $REPO = '{"name":"' + $args[0] + '"}'
    curl -u e1630m:$PAT https://api.github.com/user/repos -d $REPO
    cd ~/git
    $REPO = $args[0]
    git clone git@github.com:e1630m/$REPO
    cd $REPO
    git branch -M main
    echo $null >> README.md
    git add README.md
    git commit -S -m "Initial Commit README.md"
    git push -u origin main
}

Function gpriv {
    $PAT = 'ghp_personal_access_tokens_of_your_GitHub_account'
    $REPO = '{"name":"' + $args[0] + '", "private":"true"}'
    curl -u e1630m:$PAT https://api.github.com/user/repos -d $REPO
    cd ~/git
    $REPO = $args[0]
    git clone git@github.com:e1630m/$REPO
    cd $REPO
    git branch -M main
    echo $null >> README.md
    git add README.md
    git commit -S -m "Initial Commit README.md"
    git push -u origin main
}