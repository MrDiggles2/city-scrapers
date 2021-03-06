---
title: "Setup Help"
permalink: /docs/setup-help/
excerpt: "Intro to City Scrapers"
last_modified_at: 2018-10-04T20:15:56-04:00
toc: false
---

This document covers some of the issues associated with first-time development environment setup and with collaboration using Git.

## GitHub

### Creating a GitHub account

If you do not have an account already, go to [GitHub](https://github.com){:target="\_blank"} and sign up for an account.

### Installing Git

Please refer to the [installation guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git){:target="\_blank"} according to your operating system to install Git.

### Git 101

For a primer on Git for first-time users, see the [try.github.io](https://try.github.io/levels/1/challenges/1){:target="\_blank"} or watch the [following video](https://www.youtube.com/watch?list=PLyCZ96_3y5LXfPVZkHjhHRuIWhcjvCyQA&v=m_MjzgvVZ28){:target="\_blank"} on how to (1) find an issue, (2) fork the code, (3) edit code, (4) open a pull request.

Once you have forked the code and have begun contribution, [syncing your fork](https://help.github.com/articles/syncing-a-fork/){:target="\_blank"} periodically with the main City Bureau repository will be useful in staying up-to-date with the project.

1. You must first [add a remote link](https://help.github.com/articles/configuring-a-remote-for-a-fork/){:target="\_blank"} from which Git can track the main City Bureau project. The remote URL is `<https://github.com/City-Bureau/city-scrapers.git>`. Conventionally we name this remote source `upstream`. The remote source for your original cloned repository is usually named `origin`.

```shell
$ git remote add upstream https://github.com/City-Bureau/city-scrapers.git
```

You can see your existing remotes as well by running `git remote -v`.

2. Once you've added the City Bureau remote, fetch the changes from upstream

```shell
$ git fetch upstream
```

3. Make sure you are in the branch you hope to merge changes into (typically your `master` branch), then merge the changes in from the `upstream/master` branch.

```shell
$ git checkout master
$ git merge upstream/master
```

4. The final step is to update your fork on Github with the changes from the original repository by running `git push`.

## Creating a virtual environment

The [following gist](https://gist.github.com/bonfirefan/c5556ca54e8bbe9d83764730c36a4b3e){:target="\_blank"} covers common headaches with setting up a virtual environment on a Linux-like environment.

It is also possible to use `venv` to create your virtual environment.

```shell
$ python3.6 -m venv venv
$ source venv/bin/activate
```

Here we are naming the virtual environment `venv`, which has been added to the project's `.gitignore` file.
