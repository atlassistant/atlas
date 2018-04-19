Writing an SDK
===

If you wish to contribute to **atlas** by developing a SDK in your prefered language, here are the things to consider.

You must at least expose:
- a `ChannelClient`: Register to the broker to receive channel related topics. It should offer an easy way to create a new channel type so people can add many ways to interact with **atlas**.
- a `SkillClient`: Exposes stuff to create skills with auto discovery response. It should give an easy way for new developers to add their own skill to **atlas**

You must also check, in the `atlas/discovery/ping` handler if the atlas version is supported by your SDK. If not, you must inform the SDK developer!