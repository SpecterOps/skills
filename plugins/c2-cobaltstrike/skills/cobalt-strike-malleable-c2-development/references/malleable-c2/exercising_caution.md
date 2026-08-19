# Exercising Caution with Malleable C2

Malleable C2 gives you a new level of control over your network and host indicators. With this power also comes responsibility. Malleable C2 is an opportunity to make a lot of mistakes too. Here are a few things to think about when you customize your profiles:

- Each Cobalt Strike instance uses one profile at a time. If you change a profile or load a new profile, previously deployed Beacons cannot communicate with you.
- Always stay aware of the state of your data and what a protocol will allow when you develop a data transform. For example, if you base64 encode metadata and store it in a URI parameter— it’s not going to work. Why? Some base64 characters (+, =, and /) have special meaning in a URL. The c2lint tool and Profile Compiler will not detect these types of problems.
- Always test your profiles, even after small changes. If Beacon can’t communicate with you, it’s probably an issue with your profile. Edit it and try again.
- Trust the c2lint tool. This tool goes above and beyond the profile compiler. The checks are grounded in how this technology is implemented. If a c2lint check fails, it means there is a real problem with your profile.
