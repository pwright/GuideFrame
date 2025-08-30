from guideframe.selenium import *  # selenium helpers
from guideframe.assembly import assemble
from guideframe.utils import guide_step, get_env_settings

"""markdown
## Step 1
Skupper is a powerful layer 7 service interconnect. With Skupper, you can easily connect your applications across platforms and regions, ensuring secure communication no matter where you have them running. To get a better grasp of how it works, we'll set up a distributed system with components that aren't accessible from the outside.

Let's dive in. A company located in North America uses a public cloud provider to run their applications in a Kubernetes cluster. They need to run a front-end application on a particular namespace in this cluster. But for this application to work, it needs access to a payment processor microservice and to a database. But those are currently running on private networks.

The payment processor microservice runs on a private cloud provider in Europe and it's not public. The database is running on a bare metal Linux machine in South America. What's great about Skupper is that it doesn't require network changes, making it incredibly simple and easy to test out and integrate with your applications.

To install it in your Kubernetes cluster, all you need to do is just apply the install YAML which is available on the Skupper website. The Skupper controller watches all namespaces in your cluster for a set of custom resources and the most relevant ones are the site resource - it's the main and mandatory one.

When a site is created, the Skupper controller creates a Skupper router instance in the same namespace. The Skupper router is the core component that links your sites and routes all the traffic between the apps in your virtual application network or VAN.

Listeners are used to provide access to workloads exposed through the VAN. In a Kubernetes cluster, a service will be created to allow apps to communicate with exposed workloads. Connectors are used to expose workloads into the VAN so that they are accessible to other sites that have a corresponding listener. Listeners and connectors will match based upon the provided routing key which is just an arbitrary string.

Let's explore which resources are needed in each region. Starting with North America, the first resource needed is the site. Once a site is created, an instance of Skupper router will be created by the controller into the namespace. Then we need two listeners, one to the payment processor microservice and one to the database. Once the listeners are processed by the controller, Kubernetes services will be created into the namespace for each one.

Moving on to Europe, we need to have a site resource and we also need a connector that points to the payment processor pods. Once the connector is processed by the controller, the payment processor microservice is exposed into the VAN. Whether you are using Kubernetes or working outside of Kubernetes with Podman, Docker or even a bare metal Linux machine, Skupper has you covered.

That is the case for the database we have running in South America. It's running on a bare metal Linux machine. Similarly, we can create our resources on the file system and use the available Skupper tooling to run your Skupper site outside of Kubernetes. To expose the database into the VAN, we need a site and a connector that points to the IP and port of the database server.

At this point, the sites are individually configured, but they're not linked yet. Let's connect the Skupper network. First, we need to create a token to the public cloud cluster in North America. To do that, we create a resource named access grant. The controller processes the access grant definition and generates an access token.

Then we need to apply these access tokens into the other two sites. Skupper processes the access tokens on those sites creating a mutual TLS connection with the North America site ensuring a secure communication between the sites. Once the links are established, the VAN is working and the exposed workloads are available to the front end.

And this is how easy Skupper works. I hope you found this useful and that you're ready to start your Skupper journey.
"""

def guideframe_script():
    driver = None
    try:
        # Setup
        env = get_env_settings()
        driver_location = env["driver_location"]
        driver = driver_setup(driver_location)
        set_window_size(driver)
        
        # Step 1 - Play maximized YouTube video
        guide_step(
            1,
            lambda: open_url(driver, "https://www.youtube.com/watch?v=pm8OP9bG2mU"),
            order="action-before-vo",
        )
        
        # Wait for page to load and handle any consent popups
        sleep_for(3)  # Give the page time to fully load
        
        # Try to handle common YouTube consent popups
        try:
            # Look for and click consent buttons (common selectors)
            consent_selectors = [
                "button[aria-label*='Accept']",
                "button[aria-label*='Accept all']", 
                "button:contains('Accept')",
                "button:contains('Accept all')",
                ".ytd-consent-bump-v2-lightbox button",
                "[aria-label='Accept the use of cookies and other data for the purposes described']"
            ]
            
            for selector in consent_selectors:
                try:
                    element = driver.find_element("css selector", selector)
                    element.click()
                    sleep_for(1)  # Wait for popup to close
                    break
                except:
                    continue
        except:
            pass  # Continue if no consent popup found
        
        # Wait for voiceover to complete (approximately 6 minutes)
        import time
        time.sleep(360)  # 6 minutes = 360 seconds
        
    finally:
        print("Script complete -> moving to assembly")
        if driver:
            driver.quit()

if __name__ == "__main__":
    guideframe_script()
    assemble(1)
