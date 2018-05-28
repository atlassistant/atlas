/**
 * Encapsulates all stuff related to STT and TTS.
 */
export default class SpeechService {

  /**
   * Instantiates a new SpeechService
   * 
   * @param {String} lang 
   * @param {Function} on_start_listening 
   * @param {Function} on_end_listening 
   */
  constructor(lang, on_start_listening, on_end_listening) {
    this.speaker = new SpeechSynthesisUtterance();
    this.speaker.lang = lang;
    
    if ('webkitSpeechRecognition' in window) {
      this.start_sound = new Audio('/public/start_of_input.wav');
      this.end_sound = new Audio('/public/end_of_input.wav');

      this.recognition = new webkitSpeechRecognition();
      this.recognition.lang = lang;

      this.recognition.onstart = () => {
        this.start_sound.play();
        on_start_listening();
      };

      this.recognition.onend = this.recognition.onerror = () => {
        this.end_sound.play();
        on_end_listening();
      };

      this.recognition.onresult = (evt) => {
        if (evt.results.length > 0) {
          const r = evt.results[0];

          if (r.length > 0 && r.isFinal) {
            on_end_listening(r[0].transcript);
          }
        }
      }
    }
  }

  /**
   * Updates the service locales
   * 
   * @param {String} newlang 
   */
  changeLocale(newlang) {
    this.speaker.lang = newlang;

    if (this.recognition) {
      this.recognition.lang = newlang;
    }
  }

  /**
   * Starts the STT engine to capture audio.
   */
  listen() {
    if (!this.recognition) {
      return;
    }

    this.recognition.start();
  }

  /**
   * Cancel the listening
   */
  cancel() {
    if (!this.recognition) {
      return;
    }
    
    this.recognition.abort();
  }

  /**
   * Say something to the user
   * 
   * @param {String} text 
   * @param {Boolean} listen_on_end 
   */
  speak(text, listen_on_end=false) {
    if (!text) {
      return;
    }

    this.speaker.text = text;

    if (listen_on_end) {
      this.speaker.onend = () => {
        this.listen();
        this.speaker.onend = null;
      };
    }

    speechSynthesis.speak(this.speaker);
  }

}
