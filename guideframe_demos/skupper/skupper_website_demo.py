from guideframe.selenium import *  # selenium helpers (unchanged import)
from guideframe.assembly import assemble
from guideframe.utils import guide_step, get_env_settings

"""markdown
## Step 1
We’re switching to Skupper, specifically v2. Skupper is a layer-7 service interconnect for multi-cluster and hybrid. This walkthrough orients you on what’s new in v2 and where to find install, reference, and docs.

## Step 2
Start at the Skupper v2 landing page. It centralizes v2 overview, install commands, links to examples, and the v2 documentation set.

## Step 3
Open the v2 overview. v2 is a substantial change from v1, improving the model around sites, links, listeners, and connectors. It’s the baseline for everything that follows.

## Step 4
Ease of install, Kubernetes side: it’s a single, transparent apply of the v2 controller CRDs. We’ll open the v2 installation YAML to show exactly what you’d be applying.

## Step 5
Ease of install, CLI side: it’s a one-liner curl | sh to install the v2 CLI. This is convenient for demos; for pinned versions or air-gapped you can fetch from releases.

## Step 6
Installation details page: shows controller install options—YAML direct, Helm chart, or Operator—plus where the CLI fits for Kubernetes versus local systems.

## Step 7
“Getting started” gives you the short path: install CLI, select namespaces/contexts, install controller, then create sites, issue a token, redeem, and expose services.

## Step 8
Open the v2 CLI reference: the command surface for sites, tokens and links, system operations, and service exposure (listeners and connectors). This is the canonical source for flags and behaviors.

## Step 9
Open the v2 API/resources reference: Site, Link, Listener, Connector, and related CRDs. If you prefer declarative workflows or code generation, this is where the schema lives.

## Step 10
Drill into the Site resource. Sites are the foundation—one active Site per namespace. Review key spec fields like linkAccess and HA.

## Step 11
Open the Link resource. Links connect sites using mutual TLS. In practice you rarely craft these by hand—tokens handle the safe issuance path.

## Step 12
Open the Listener command docs. Listeners are the client-side endpoints you expose locally; they route by key to remote connectors.

## Step 13
Open the Connector command docs. Connectors bind your server workloads to matching listener routing keys in other sites.

## Step 14
Jump to a v2 Hello-World example repo. It shows the minimal cross-cluster app and where Skupper is introduced in the flow.

## Step 15
Highlight the install snippets in that example: controller install via v2 install.yaml and CLI via v2 install.sh, then site create, token issue/redeem.

## Step 16
Observability: the Network console. It’s a Helm-installed observer for topology, services, sites, and flows. Useful for demos and ops.

## Step 17
Security and policy: Skupper policies let you default-deny and explicitly allow service-network flows. Good to know when you’re hardening.

## Step 18
Troubleshooting a service network: tips by symptom and a pointer to debug commands and dumps.

## Step 19
Install troubleshooting: common local path and permissions issues for the CLI installer.

## Step 20
Open the “system install” command details. Useful for local platforms (Podman/Docker/Linux) and for understanding what the CLI configures.

## Step 21
Open the “token issue” details. This is the normal path for creating a link securely—short-lived, single-use by default.

## Step 22
Open the “listener create” details so you can see required args, status waits, and the routing-key semantics.

## Step 23
Return to the v2 landing notes: v2 is not backward-compatible with v1. Expect a short downtime window during upgrade while v1 shuts down and v2 starts.

## Step 24
Open the Releases page to confirm current versions and cross-link back to v2. Handy when pinning.

## Step 25
Open the Skupper GitHub org for deeper dives, issues, and additional examples.

## Step 26
Back to the v2 Hello-World example: highlight the linking steps for a clear mental model—issue token in one site, redeem in the other.

## Step 27
Still in the example: highlight the exposure steps—listener on the client side, connector on the server side, matching routing key.

## Step 28
Wrap-up: v2 landing page again—single place to remember: overview, install commands, docs, examples.

## Step 29
Open the v2 docs home to reinforce the structure: Basics, Installation, CLI on Kubernetes, YAML, and Observability.

## Step 30
Final note: install is simple, docs are coherent, and the reference is explicit. If you script against the CLI or generate CRDs, v2’s model is easier to automate.
"""

def guideframe_script():
    driver = None
    try:
        # Setup
        env = get_env_settings()
        driver_location = env["driver_location"]
        driver = driver_setup(driver_location)
        set_window_size(driver)
        open_url(driver, "https://skupper.io/")

# ------------------- Overview ------------------- #

        # Step 1 - Skupper intro
        guide_step(1, lambda: None)

        # Step 2 - v2 landing
        guide_step(2,
            lambda: open_url(driver, "https://skupper.io/v2/index.html"),
            order="action-before-vo"
        )

        # Step 3 - v2 overview
        guide_step(3,
            lambda: open_url(driver, "https://skupper.io/v2/overview.html"),
            order="action-before-vo"
        )

        # Step 4 - show install YAML via docs page (renders inline; no download)
        guide_step(
            4,
            lambda: open_url(driver, "https://skupperproject.github.io/skupper-docs/install/index.html"),
            order="action-before-vo"
        )
        
        # Step 5 - show CLI install instructions (renders inline; no download)
        guide_step(
            5,
            lambda: open_url(driver, "https://skupperproject.github.io/skupper-docs/cli/install.html"),
            order="action-before-vo"
        )
        # Step 6 - Installation details page
        guide_step(6,
            lambda: open_url(driver, "https://skupperproject.github.io/skupper-docs/install/index.html"),
            order="action-before-vo"
        )

        # Step 7 - Getting started (short path)
        guide_step(7,
            lambda: open_url(driver, "https://skupper.io/start/"),
            order="action-before-vo"
        )

# ------------------- Docs & Reference ------------------- #

        # Step 8 - CLI reference index
        guide_step(8,
            lambda: open_url(driver, "https://skupperproject.github.io/refdog/commands/"),
            order="action-before-vo"
        )

        # Step 9 - API/resources reference index
        guide_step(9,
            lambda: open_url(driver, "https://skupperproject.github.io/refdog/resources/"),
            order="action-before-vo"
        )

        # Step 10 - Site resource
        guide_step(10,
            lambda: open_url(driver, "https://skupperproject.github.io/refdog/resources/site.html"),
            order="action-before-vo"
        )

        # Step 11 - Link resource
        guide_step(11,
            lambda: open_url(driver, "https://skupperproject.github.io/refdog/resources/link.html"),
            order="action-before-vo"
        )

        # Step 12 - Listener command
        guide_step(12,
            lambda: open_url(driver, "https://skupperproject.github.io/refdog/commands/listener/create.html"),
            order="action-before-vo"
        )

        # Step 13 - Connector command index
        guide_step(13,
            lambda: open_url(driver, "https://skupperproject.github.io/refdog/commands/connector/"),
            order="action-before-vo"
        )

        # Step 14 - v2 Hello World example repo
        guide_step(14,
            lambda: open_url(driver, "https://github.com/skupperproject/skupper-example-hello-world/tree/v2"),
            order="action-before-vo"
        )

        # Step 15 - Example README install snippets (highlight)
        guide_step(15,
            lambda: highlight_github_code(driver, "https://github.com/skupperproject/skupper-example-hello-world/blob/v2/README.md#L23-L31"),
            order="action-before-vo"
        )

        # Step 16 - Observability console
        guide_step(16,
            lambda: open_url(driver, "https://skupperproject.github.io/skupper-docs/console/index.html"),
            order="action-before-vo"
        )

        # Step 17 - Security policies
        guide_step(17,
            lambda: open_url(driver, "https://skupper.io/docs/policy/index.html"),
            order="action-before-vo"
        )

        # Step 18 - Troubleshooting service network
        guide_step(18,
            lambda: open_url(driver, "https://skupper.io/docs/troubleshooting/index.html"),
            order="action-before-vo"
        )

        # Step 19 - Install troubleshooting
        guide_step(19,
            lambda: open_url(driver, "https://skupper.io/install/troubleshooting.html"),
            order="action-before-vo"
        )

        # Step 20 - System install command (local platforms)
        guide_step(20,
            lambda: open_url(driver, "https://skupperproject.github.io/refdog/commands/system/install.html"),
            order="action-before-vo"
        )

        # Step 21 - Token issue details
        guide_step(21,
            lambda: open_url(driver, "https://skupperproject.github.io/refdog/commands/token/issue.html"),
            order="action-before-vo"
        )

        # Step 22 - Listener create details
        guide_step(22,
            lambda: open_url(driver, "https://skupperproject.github.io/refdog/commands/listener/create.html"),
            order="action-before-vo"
        )

        # Step 23 - v2 incompatibility note (return to v2 landing)
        guide_step(23,
            lambda: open_url(driver, "https://skupper.io/v2/index.html"),
            order="action-before-vo"
        )

        # Step 24 - Releases (confirm versions)
        guide_step(24,
            lambda: open_url(driver, "https://skupper.io/releases/index.html"),
            order="action-before-vo"
        )

# ------------------- Examples Deep Dive ------------------- #

        # Step 25 - GitHub org
        guide_step(25,
            lambda: open_url(driver, "https://github.com/skupperproject"),
            order="action-before-vo"
        )

        # Step 26 - Example: linking steps (highlight)
        guide_step(26,
            lambda: highlight_github_code(driver, "https://github.com/skupperproject/skupper-example-hello-world/blob/v2/README.md#L26-L33"),
            order="action-before-vo"
        )

        # Step 27 - Example: exposure steps (highlight)
        guide_step(27,
            lambda: highlight_github_code(driver, "https://github.com/skupperproject/skupper-example-hello-world/blob/v2/README.md#L34-L41"),
            order="action-before-vo"
        )

# ------------------- Conclusion ------------------- #

        # Step 28 - Back to v2 landing (one-stop hub)
        guide_step(28,
            lambda: open_url(driver, "https://skupper.io/v2/index.html"),
            order="action-before-vo"
        )

        # Step 29 - v2 docs home
        guide_step(29,
            lambda: open_url(driver, "https://skupperproject.github.io/skupper-docs/"),
            order="action-before-vo"
        )

        # Step 30 - Final recap page (home)
        guide_step(30,
            lambda: open_url(driver, "https://skupper.io/"),
            order="action-before-vo"
        )

    finally:
        print("Script complete -> moving to assembly")
        if driver:
            driver.quit()

if __name__ == "__main__":
    guideframe_script()
    assemble(30)

