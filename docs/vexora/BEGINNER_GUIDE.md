# Beginner guide: get a VEXORA AppImage built on GitHub

You do not need to install anything. GitHub builds the app on its own computers. Nothing here asks
for a password or token in chat.

## What to expect (read first)
- The **first run can fail**. A missing system package or a compile error is normal for a first build.
  A failure is useful: the run tells us exactly what broke. Fixing it is the next step, not a disaster.
- The build is big (a Rust project with ~26 crates). Expect **roughly 1 to 3+ hours** per run.
  (This is an estimate; no run has happened yet.)
- **Cost:** a *private* repo on a free GitHub plan gets 2,000 Linux minutes per month. One long run can use
  a large part of that. Public repos get free minutes. Check *Settings > Billing and plans* first.
- A green run means the *baseline* builds and its checks pass. It does **not** mean VEXORA's new features
  exist. They do not exist yet (see README "Honest status").

## Step 1: create an empty repository
1. Sign in at github.com. Click **+** (top right) > **New repository**.
2. Name: `vexora`. Choose **Private** (or Public, see cost note above).
3. Leave **everything else unticked**: no README, no .gitignore, no license. Click **Create repository**.
4. Copy the page address, like `https://github.com/YOUR-NAME/vexora`.

## Step 2: give Claude the URL and access
1. Paste only that URL in the chat.
2. Claude will ask for access to that repository. **Approve it in the prompt that appears** (it must allow
   *push*). Never paste a password or token into the chat.

## Step 3: Claude uploads the project
Claude pushes the project and the workflow to your repository and tells you when it is done.
You can check: your repo page should show folders such as `crates`, `apps`, `branding`, `.github`.

## Step 4: start the build
1. Open your repo on github.com > the **Actions** tab.
2. If you see a green button **"I understand my workflows, go ahead and enable them"**, click it.
3. In the left list click **VEXORA build (Linux x86_64)**.
4. Click **Run workflow** (right side). Leave the defaults:
   - *Run the baseline test suite*: ticked (slower but honest).
   - *Runner image*: `ubuntu-24.04`. Pick `ubuntu-22.04` only if the AppImage must run on older Linux.
5. Click the green **Run workflow** button. A new yellow row appears: that is your build.

## Step 5: read the result
Click the row. When it finishes:
- **Green check**: every stage succeeded (fetch, build, tests, packaging, startup checks).
- **Red X**: at least one stage failed. Open the run, then the **Summary** page. The **BUILD_REPORT** table
  lists each stage as PASSED/FAILED. Click the failed step to see its log.
- Orange/yellow: still running. Closing the browser does not stop it.

## Step 6: download and check the files
At the bottom of the run page, under **Artifacts**:
- `VEXORA-baseline-zip-tests-passed` (or `...-FAILED` / `...-not-run`): the ZIP with the AppImage, licences,
  report and logs. The name says what the tests did.
- `VEXORA-baseline-appimage-and-source`: the raw AppImage, a `.tar.gz`, and a source ZIP.
- `VEXORA-build-logs`: the report and every log (always present, even if the build failed).

Downloads arrive as a `.zip`; unzip it. Then on a Linux x86_64 PC, in a terminal:
```bash
sha256sum -c SHA256SUMS              # every line should say OK
chmod +x VEXORA-baseline-*.AppImage
./VEXORA-baseline-*.AppImage
```
It needs a glibc at least as new as the runner (Ubuntu 24.04 image = glibc 2.39). If it will not start:
`./VEXORA-baseline-*.AppImage --appimage-extract-and-run`. If your Linux is older, rerun with `ubuntu-22.04`.

**What you will see:** the window still says VectorCraft inside the app, and the VEXORA icon is white, so it is
hard to see on a light launcher. That is expected for the baseline.

## If it fails
1. Open the `VEXORA-build-logs` artifact. Send Claude `BUILD_REPORT.md` and the log of the failed step
   (usually `01-fetch.log`, `02-build.log`, `03-test.log` or `04-package.log`). Logs hold no secrets.
2. Claude reads the real error, fixes it, and you run the workflow again (Step 4).

## What "success" would and would not prove
Proved by a green run: the code compiled on Ubuntu, the tests passed on the runner, an AppImage exists,
it extracts, its CLI prints a version, it shows the VEXORA icon, and the GUI stayed up for 25 seconds under a
virtual screen. Not proved: drawing, saving, exporting, keyboard and mouse use, high-DPI, other distributions.
Those need hands-on testing on a real desktop.
