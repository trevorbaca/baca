Brewing Guile
=============

Install instructions returned by "install guile on mac" suggest two steps:

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" < /dev/null 2> /dev/null

Brew is already installed on my machine:

    $ which brew
    /usr/local/bin/brew

So I decided to skip the first step.

I deactivated my usual virtualenv:

    $ deactivate

Then I brewed Guile:

    $ brew install guile
    Updating Homebrew...

Brew took a minute, or even two, to update itself, without messaging.

Then Brew came back with a bunch of stuff, but failed:

    Fast-forwarded master to origin/master.
    ==> Downloading https://homebrew.bintray.com/bottles-portable-ruby/portable-ruby-2.6.3_2.yosemite.bottle.tar.gz
    ######################################################################## 100.0%
    ==> Pouring portable-ruby-2.6.3_2.yosemite.bottle.tar.gz
    ==> Homebrew has enabled anonymous aggregate formula and cask analytics.
    Read the analytics documentation (and how to opt-out) here:
    https://docs.brew.sh/Analytics
    No analytics have been recorded yet (or will be during this `brew` run).

    ==> Homebrew is run entirely by unpaid volunteers. Please consider donating:
    https://github.com/Homebrew/brew#donations
    ==> Auto-updated Homebrew!
    Updated 1 tap (homebrew/core).
    ==> New Formulae
    abseil                                        libirecovery
    acl2                                          libkeccak
    < ... snip ... >

    /usr/local/Homebrew/Library/Homebrew/brew.rb:17:in `<main>': HOMEBREW_REQUIRED_RUBY_VERSION was not exported! Please call bin/brew directly! (RuntimeError)

So now I face a choice: call /usr/local/bin/brew (as indicated in Brew's error
messaging)? Or run the bit of Ruby suggested online?

    $ brew --version
    Homebrew 2.5.11
    Homebrew/homebrew-core (git revision 93ca3; last commit 2020-11-18)

    $ /usr/local/bin/brew --version
    Homebrew 2.5.11
    Homebrew/homebrew-core (git revision 93ca3; last commit 2020-11-18)

This is current as of today. So I'll call Brew directly. Which gets a lot further.
But fails because of the version of Xcode installed on the machine:

    ~$ /usr/local/bin/brew install guile
    ==> Downloading https://homebrew.bintray.com/bottles/bdw-gc-8.0.4.mojave.bottle.tar.gz
    ==> Downloading from https://d29vzk4ow07wi7.cloudfront.net/05219d7d030791e3c3e3751b36a603a
    ######################################################################## 100.0%
    ==> Downloading https://homebrew.bintray.com/bottles/gmp-6.2.1.mojave.bottle.tar.gz
    ==> Downloading from https://d29vzk4ow07wi7.cloudfront.net/00fb998dc2abbd09ee9f2ad733ae1ad
    ######################################################################## 100.0%
    ==> Downloading https://homebrew.bintray.com/bottles/libffi-3.3.mojave.bottle.tar.gz
    ######################################################################## 100.0%
    ==> Downloading https://homebrew.bintray.com/bottles/libtool-2.4.6_2.mojave.bottle.tar.gz
    ==> Downloading from https://d29vzk4ow07wi7.cloudfront.net/77ca68934e7ed9b9b0b8ce17618d7f0
    ######################################################################## 100.0%
    ==> Downloading https://homebrew.bintray.com/bottles/libunistring-0.9.10.mojave.bottle.tar
    ==> Downloading from https://d29vzk4ow07wi7.cloudfront.net/1d0c8e266acddcebeef3d9f6162d6f7
    ######################################################################## 100.0%
    ==> Downloading https://homebrew.bintray.com/bottles/pkg-config-0.29.2_3.mojave.bottle.tar
    ==> Downloading from https://d29vzk4ow07wi7.cloudfront.net/0d14b797dba0e0ab595c9afba8ab7ef
    < ... snip ...>
    ==> Summary
    🍺  /usr/local/Cellar/sqlite/3.33.0: 11 files, 4MB
    ==> Installing graphviz dependency: xz
    ==> Pouring xz-5.2.5.mojave.bottle.tar.gz
    🍺  /usr/local/Cellar/xz/5.2.5: 92 files, 1.1MB
    ==> Installing graphviz dependency: python@3.9
    Error: Xcode alone is not sufficient on Mojave.
    Install the Command Line Tools:
    xcode-select --install

So I do as Brew suggests:

    $ xcode-select --install
    xcode-select: note: install requested for command line developer tools

This pops a modal with three buttons: "Get XCode," "Not now," "Install."
With "Install" highlighted.

I click "Install." A second window to agree to terms. A third window prompting
me to connect the laptop to a power source. A fourth window showing a 2-minute
progress indicator titled "Installing software." A fifth window saying "The
software was installed." with a "Done" button. I click "Done."

I try to brew again:

    $ /usr/local/bin/brew install guile
    Warning: guile 3.0.4 is already installed and up-to-date
    To reinstall 3.0.4, run `brew reinstall guile`

Which is frustrating. But possibly correct:

    $ which guile
    /usr/local/bin/guile

    $ guile --version
    guile (GNU Guile) 3.0.4

So maybe the XCode update wasn't necessary? Who knows.

I restart Terminal and confirm that Guile 3.0.4 is available in my virtuanlenv.
