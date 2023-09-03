/* eslint-disable jsx-a11y/media-has-caption */
import axios from 'axios';
import { CircleNotch } from 'phosphor-react';
import { FormEvent, useEffect, useRef, useState } from 'react';
import { BACKEND_URL } from '../constants';

function Braille() {
  const [url, setUrl] = useState<string>();
  const [isSubmitLoading, setIsSubmitLoading] = useState(false);

  const [pdfText, setPdfText] = useState<string>();
  const [braille, setBraille] = useState<string>();

  const submitForm = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitLoading(true);

    axios
      .get(`${BACKEND_URL}/braille/url?url=${url}`)
      .then((response) => {
        setPdfText(response.data.text);
        setBraille(response.data.braille);
        setIsSubmitLoading(false);
      })
      .catch((err) => {
        console.log(err);
        setIsSubmitLoading(false);
      });
  };

  return (
    <div className="narration braille">
      <div className="title">Braille</div>
      <form onSubmit={submitForm}>
        <div className="item-group">
          <div className="form-item form-item-long">
            <div className="label">Please enter the pdf link here</div>
            <input type="url" value={url} onChange={(event) => setUrl(event.target.value)} />
          </div>
        </div>
        <button className="submit" disabled={isSubmitLoading} type="submit">
          Submit {isSubmitLoading && <CircleNotch />}
        </button>
      </form>
      {!isSubmitLoading && pdfText && (
        <>
          <div className="text-display">{pdfText}</div>
          <div className="text-display braille-text">{braille}</div>
        </>
      )}
    </div>
  );
}

export default Braille;
