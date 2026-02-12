# Geha Research Group Site 
Go to our group site at:

[https://geha-group.github.io](https://geha-group.github.io)

## Editing This Site

This site is built with **Jekyll** and deployed via **GitHub Pages**. You should preview changes locally before pushing (see Sec. 2 and 3). Most contributors will not have direct push access to this repository. Please use the fork + pull request workflow.

### 1. Fork the Repository

On GitHub:
- Go to: https://github.com/geha-group/geha-group.github.io
- Click Fork (top right).
- This creates your own copy under your GitHub account.

Now, you need to clone your fork to have a local copy you can edit: 

```bash
git clone git@github.com:geha-group/geha-group.github.io.git
cd geha-group.github.io
```

If you anticipate making multiple rounds of changes over time (and multiple pull reqeusts to merge edits back into the main website), you shuold make a new branch in your fork. If you are making only a few minimal edits, you can just edit in the main branch of your fork and merge back into the main branch of the website. 

Before making changes, you can create a branch like this 

```bash
git checkout -b your-new-branch-name
```

---

### 2. Install Dependencies

Make sure you have Ruby and Bundler installed.

Then run:

```bash
bundle install
```

This installs all required gems from the `Gemfile`.

---

### 3. Serve Locally

To preview the site locally:

```bash
bundle exec jekyll serve --watch
```

Then open:

```
http://localhost:4000
```

The site will auto-rebuild when you save changes, so you can start editing and see how your changes look. 

If it doesn’t update, stop (`Ctrl+C`) and restart the server.

---

### 4. Making Edits

This site follows a pretty standard jekyll structure. In general, you can modify the following components by editing the corresponding files: 
* **Pages** → Edit `.html` or `.md` files in the corresponding directory.
* **Layouts** → `_layouts/`
* **Includes (nav, footer, etc.)** → `_includes/`
* **Site settings** → `_config.yml`
* **Styling** → `assets/css/` or `_sass/` files.

When creating new pages, make sure all pages include some front matter, e.g.:

```yaml
---
layout: default
title: Page Title
---
```

### How to add yourself (or a new person) to the Members page

Member “cards” are generated automatically from **collection files** (one file per person). To add a new member, you just (1) add a card file in the right folder and (2) add a photo in the images folder.

**1) Pick the correct member category**

Add a new file to the collection folder that matches your role:

* **Postdocs** → `_postdocs/`
* **Graduate Students** → `_grads/`
* **Undergrads** → `_undergrads/`

**2) Create a new “card” file**

In the correct folder above, create a new file named something like:

* `_grads/jane-doe.md`

Use this template:

```yaml
---
layout: page
title: "Full Name" # this must match the name you publish under for the ADS search to work
image: "/assets/images/jane-doe.jpg"   # path to your photo
external_url: https://example.com      # optional (personal website / scholar / etc.)
text: |
  1–2 sentence description that appears on the card.
---
```
**3) Add the profile photo**

Put the image file here:

```
assets/images/
```

Then set the `image:` field to match, e.g.:

```yaml
image: "/assets/images/jane-doe.jpg"
```

Recommended: use an image that matches the aspect ratio of everyone else's cards (618 × 796). 

---

### 5. Commit & Push to Your Fork 

Once satisfied with changes:

```bash
git add .
git commit -m "Describe your changes"
git push origin your-new-branch-name
```

### 6. Open a Pull Request

- Go to your fork on GitHub.
- Click Compare & pull request.
- Make sure the base repository is: geha-group/geha-group.github.io 
- Submit the pull request

Once approved, your changes will be merged and automatically deployed.