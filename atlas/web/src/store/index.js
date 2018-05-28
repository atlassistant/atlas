import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import { SpeechService, WsService } from './../services';

Vue.use(Vuex);

let speechService = null;
let wsService = null;

const state = {
  lang: null,
  messages: [],
  isThinking: false,
  isConnected: false,
  isListening: false,
  isTextInput: false,
};

const getters = {
  lang: state => state.lang,
  messages: state => state.messages,
  isThinking: state => state.isThinking,
  isConnected: state => state.isConnected,
  isListening: state => state.isListening,
  isTextInput: state => state.isTextInput,
};

const mutations = {
  setLang(state, lang) {
    if (lang) {
      state.isConnected = true;
    } else {
      state.isConnected = false;
    }

    state.lang = lang;
  },
  setThinking(state, isThinking) {
    state.isThinking = isThinking;
  },
  setIsTextInput(state, isTextInput) {
    state.isTextInput = isTextInput;
  },
  setListening(state, isListening) {
    state.isListening = isListening;
  },
  pushMessage(state, data) {
    state.messages.push({
      id: state.messages.length + 1,
      ...data,
    });
  },
};

export const actions = {
  setLocale({ commit, dispatch }, locale) {
    if (!speechService) {
      speechService = new SpeechService(locale, () => commit(mutations.setListening.name, true),
        text => {
          commit(mutations.setListening.name, false);
          dispatch(actions.parse.name, text);
        });
    } else {
      speechService.changeLocale(locale);
    }

    commit(mutations.setLang.name, locale);
  },
  startThinking({ commit }) {
    commit(mutations.setThinking.name, true);
  },
  stopThinking({ commit }) {
    commit(mutations.setThinking.name, false);
  },
  disconnect({ commit }) {
    commit(mutations.setLang.name, null);
  },
  ask({ commit, state }, payload) {
    commit(mutations.setThinking.name, false);
    commit(mutations.pushMessage.name, payload);

    speechService.speak(payload.text, !state.isTextInput);
  },
  show({ commit }, payload) {
    commit(mutations.pushMessage.name, payload);

    speechService.speak(payload.text);
  },
  parse({ commit }, text) {
    if (!text) {
      return;
    }

    commit(mutations.pushMessage.name, {
      client: true,
      text,
    });

    wsService.parse(text);
  },
  switchToTextInput({ commit }) {
    speechService.cancel();
    commit(mutations.setIsTextInput.name, true);
  },
  listen({ commit }) {
    commit(mutations.setIsTextInput.name, false);
    speechService.listen();
  },
};

export default function createStore() {
  const store = new Vuex.Store({
    state,
    getters,
    mutations,
    actions,
    plugins: [createPersistedState({
      paths: ['isTextInput'],
    })],
  });

  // Creates the service used to access websockets
  wsService = new WsService(
    data => store.dispatch(actions.ask.name, data),
    data => store.dispatch(actions.show.name, data),
    () => store.dispatch(actions.stopThinking.name),
    () => store.dispatch(actions.startThinking.name),
    data => store.dispatch(actions.setLocale.name, data.lang),
    () => store.dispatch(actions.disconnect.name));

  return store;
}
