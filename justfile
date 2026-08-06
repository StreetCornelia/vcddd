set shell := ["bash", "-cu"]
set export

target-branch := "develop/2.x"
main-branch := "main"

# Stash changes, switch to develop/2.x, restore them, and create a local commit.
commit message:
    #!/usr/bin/env bash
    set -euo pipefail

    target_branch='{{target-branch}}'
    current_branch="$(git branch --show-current)"
    stash_created=false

    if [[ "$current_branch" != "$target_branch" ]]; then
        if [[ -n "$(git status --porcelain)" ]]; then
            git stash push --include-untracked --message "just commit: temporary stash"
            stash_created=true
        fi

        git switch "$target_branch"

        if [[ "$stash_created" == true ]]; then
            git stash pop
        fi
    fi

    if [[ -z "$(git status --porcelain)" ]]; then
        echo "没有可提交的改动。" >&2
        exit 1
    fi

    commit_message="$message"
    if [[ -z "${commit_message//[[:space:]]/}" ]]; then
        echo "commit message 不能为空。" >&2
        exit 1
    fi

    git add --all
    git commit --message "$commit_message"

# Push develop/2.x, merge it into main, push main, and return to develop/2.x.
push:
    #!/usr/bin/env bash
    set -euo pipefail

    develop_branch='{{target-branch}}'
    main_branch='{{main-branch}}'
    current_branch="$(git branch --show-current)"

    if [[ -n "$(git status --porcelain)" ]]; then
        echo "工作区存在未提交的改动，请先完成提交后再推送。" >&2
        exit 1
    fi

    if [[ "$current_branch" != "$develop_branch" ]]; then
        git switch "$develop_branch"
    fi

    git push origin "$develop_branch"
    git switch "$main_branch"
    git merge "$develop_branch"
    git push origin "$main_branch"
    git switch "$develop_branch"
