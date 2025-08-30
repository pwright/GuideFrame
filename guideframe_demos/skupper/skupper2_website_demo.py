from guideframe.selenium import *  # selenium helpers (unchanged)
from guideframe.assembly import assemble
from guideframe.utils import guide_step, get_env_settings

"""markdown
## Step 1
Welcome to the Skupper site preview. We'll get oriented to v2, show the easiest install paths, and point to the docs, references, examples, and community.

## Step 2
This gives a concise, step-by-step path using a simple multi-namespace Hello World.

## Step 3
It shows two straightforward install options: kubectl apply or Helm.

## Step 4
This is the one-liner you can use with kubectl to install the controller and CRDs.

## Step 5
It's a quick way to fetch the `skupper` binary for demos; use releases for pinning.

## Step 6
To show the structure: Introduction, Installation, Operation, and Reference.

## Step 7
This is the canonical surface for site, token/link, listener, connector, system, and debug.

## Step 8
This is usually your first CLI action in a namespace.

## Step 9
This safely produces a short-lived credential for linking sites.

## Step 10
This consumes the token at the remote site to establish a link.

## Step 11
Listeners are client-side endpoints; they pair with connectors by routing key.

## Step 12
Connectors bind server workloads; again, match routing keys with listeners.

## Step 13
This is the declarative model backing the CLI.

## Step 14
One active Site per namespace; it's the foundation.

## Step 15
This defines router-to-router connectivity; usually created via tokens.

## Step 16
Client-side endpoint exposed locally.

## Step 17
Server-side binding to local workloads or hosts.

## Step 18
It collects app examples, scenarios, platforms, and admin integrations.

## Step 19
It's the minimal, multi-service app used throughout the quickstarts.

## Step 20
Good for showing cross-cluster metrics with Skupper.

## Step 21
We'll touch the security and routing introductions—useful for framing v2.

## Step 22
Skupper uses mutual TLS and a private CA by default; services are not exposed publicly.

## Step 23
Layer-7 addressing enables multi-cluster services, balancing, and cost-based failover.

## Step 24
For creating a site with YAML on Kubernetes.

## Step 25
For creating a site with `skupper`.

## Step 26
This is the Helm-installed console for topology and flow visibility.

## Step 27
Source, issues, mailing list, and social links live here.

## Step 28
To recap the top-level messages and nav.

## Step 29
To reinforce where the declarative model lives.

## Step 30
Final note: v2 install paths are simple; the CLI and CRDs are well-documented; examples are ready to run; and the community links are obvious.
"""

def guideframe_script():
    driver = None
    try:
        # Setup
        env = get_env_settings()
        driver_location = env["driver_location"]
        driver = driver_setup(driver_location)
        set_window_size(driver)
        open_url(driver, "https://www.ssorj.net/skupper-website/")

        # ------------------- Overview ------------------- #

        # Step 1 - Home (hang for VO)
        guide_step(1, lambda: None)

        # Step 2 - Getting started
        guide_step(
            2,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/start/index.html"),
            order="action-before-vo",
        )

        # Step 3 - Install on Kubernetes (docs)
        guide_step(
            3,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/docs/installation/kubernetes.html"),
            order="action-before-vo",
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

        # Step 6 - Docs index
        guide_step(
            6,
            lambda: switch_to_tab(driver, 0),
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/docs/index.html"),
            order="action-before-vo",
        )

        # Step 7 - CLI reference index
        guide_step(
            7,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/commands/index.html"),
            order="action-before-vo",
        )

        # Step 8 - site create
        guide_step(
            8,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/commands/site/create.html"),
            order="action-before-vo",
        )

        # Step 9 - token issue
        guide_step(
            9,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/commands/token/issue.html"),
            order="action-before-vo",
        )

        # Step 10 - token redeem
        guide_step(
            10,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/commands/token/redeem.html"),
            order="action-before-vo",
        )

        # Step 11 - listener create
        guide_step(
            11,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/commands/listener/create.html"),
            order="action-before-vo",
        )

        # Step 12 - connector create
        guide_step(
            12,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/commands/connector/create.html"),
            order="action-before-vo",
        )

        # Step 13 - API reference index
        guide_step(
            13,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/resources/index.html"),
            order="action-before-vo",
        )

        # Step 14 - Site resource
        guide_step(
            14,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/resources/site.html"),
            order="action-before-vo",
        )

        # Step 15 - Link resource
        guide_step(
            15,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/resources/link.html"),
            order="action-before-vo",
        )

        # Step 16 - Listener resource
        guide_step(
            16,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/resources/listener.html"),
            order="action-before-vo",
        )

        # Step 17 - Connector resource
        guide_step(
            17,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/resources/connector.html"),
            order="action-before-vo",
        )

        # Step 18 - Examples index
        guide_step(
            18,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/examples/index.html"),
            order="action-before-vo",
        )

        # Step 19 - Hello World example (GitHub, new tab)
        guide_step(
            19,
            lambda: open_link_in_new_tab(driver, "https://github.com/skupperproject/skupper-example-hello-world"),
            order="action-before-vo",
        )

        # Step 20 - Prometheus example (GitHub, new tab)
        guide_step(
            20,
            lambda: open_link_in_new_tab(driver, "https://github.com/skupperproject/skupper-example-prometheus/tree/v2"),
            order="action-before-vo",
        )

        # Step 21 - Documentation index again
        guide_step(
            21,
            lambda: switch_to_tab(driver, 0),
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/docs/index.html"),
            order="action-before-vo",
        )

        # Step 22 - Security intro
        guide_step(
            22,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/docs/introduction/security.html"),
            order="action-before-vo",
        )

        # Step 23 - Routing intro
        guide_step(
            23,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/docs/introduction/routing.html"),
            order="action-before-vo",
        )

        # Step 24 - Using the API (site with YAML)
        guide_step(
            24,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/docs/operation/api/site-configuration.html"),
            order="action-before-vo",
        )

        # Step 25 - Using the CLI (site with skupper)
        guide_step(
            25,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/docs/operation/cli/site-configuration.html"),
            order="action-before-vo",
        )

        # Step 26 - Network Observer install
        guide_step(
            26,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/docs/installation/network-observer.html"),
            order="action-before-vo",
        )

        # Step 27 - Community page
        guide_step(
            27,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/community/index.html"),
            order="action-before-vo",
        )

        # Step 28 - Back to Home
        guide_step(
            28,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/"),
            order="action-before-vo",
        )

        # Step 29 - API reference index (reinforce)
        guide_step(
            29,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/resources/index.html"),
            order="action-before-vo",
        )

        # Step 30 - Wrap on Docs index
        guide_step(
            30,
            lambda: open_url(driver, "https://www.ssorj.net/skupper-website/docs/index.html"),
            order="action-before-vo",
        )

    finally:
        print("Script complete -> moving to assembly")
        if driver:
            driver.quit()

if __name__ == "__main__":
    guideframe_script()
    assemble(30)
