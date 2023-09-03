/* eslint-disable jsx-a11y/media-has-caption */
import axios from 'axios';
import { CircleNotch } from 'phosphor-react';
import { FormEvent, useEffect, useRef, useState } from 'react';
import { BACKEND_URL } from '../constants';

function Notes() {
  const [url, setUrl] = useState<string>();
  const [mode, setMode] = useState<string>('text');
  const [isSubmitLoading, setIsSubmitLoading] = useState(false);

  const [pdfText, setPdfText] = useState<string>();
  const [pdfAudio, setPdfAudio] = useState<string>();

  useEffect(() => {
    setPdfText(undefined);
    setPdfAudio(undefined);
  }, [url]);

  const modeInputRef = [useRef<HTMLInputElement>(null), useRef<HTMLInputElement>(null)];

  const handleModeChange = (index: number) => {
    if (modeInputRef[index].current !== null) modeInputRef[index].current?.click();
  };

  const submitForm = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitLoading(true);

    if (mode == 'text') {
      axios
        .get(`${BACKEND_URL}/notes/text?url=${url}`)
        .then((response) => {
          setPdfText(response.data);
          setIsSubmitLoading(false);
        })
        .catch((err) => {
          console.log(err);
          setIsSubmitLoading(false);
        });
    } else {
      axios
        .get(`${BACKEND_URL}/notes/narration?url=${url}`)
        .then((response) => {
          setPdfText(response.data.text);
          setPdfAudio('data:audio/ogg;base64,' + response.data.audio);
          setIsSubmitLoading(false);
        })
        .catch((err) => {
          console.log(err);
          setIsSubmitLoading(false);
        });
    }
  };

  return (
    <div className="narration notes">
      <div className="title">Note Dictation</div>
      <form onSubmit={submitForm}>
        <div className="item-group">
          <div className="form-item form-item-long">
            <div className="label">Please enter the note image link here</div>
            <input type="url" value={url} onChange={(event) => setUrl(event.target.value)} />
          </div>
        </div>
        <div className="item-group">
          <div className="form-item form-item-long">
            <div className="label">In which form do you want the note ?</div>
            <div className="radio-grp">
              <button type="button" title="text" data-checked={mode === 'text'} onClick={() => handleModeChange(0)}>
                <input
                  ref={modeInputRef[0]}
                  type="radio"
                  name="mode"
                  id="text"
                  value="text"
                  checked={mode === 'text'}
                  onChangeCapture={(event) => setMode(event.currentTarget.value)}
                />{' '}
                Text
              </button>
              <button type="button" title="audio" data-checked={mode === 'audio'} onClick={() => handleModeChange(1)}>
                <input
                  ref={modeInputRef[1]}
                  type="radio"
                  name="mode"
                  id="audio"
                  value="audio"
                  checked={mode === 'audio'}
                  onChangeCapture={(event) => setMode(event.currentTarget.value)}
                />{' '}
                Audio
              </button>
            </div>
          </div>
        </div>
        <button className="submit" disabled={isSubmitLoading} type="submit">
          Submit {isSubmitLoading && <CircleNotch />}
        </button>
      </form>
      {mode == 'audio' && !isSubmitLoading && pdfAudio && (
        <audio src={pdfAudio} controls>
          Your browser does not support the audio element.
        </audio>
      )}
      {!isSubmitLoading && pdfText && (
        <div className="image-text">
          <img className="input-note" src={url} alt="note-input" />
          <div className="text-display">{pdfText}</div>
        </div>
      )}
    </div>
  );
}

export default Notes;
