/* eslint-disable jsx-a11y/media-has-caption */
import axios from 'axios';
import { CircleNotch } from 'phosphor-react';
import { FormEvent, useState } from 'react';
import { BACKEND_URL } from '../constants';

function SignLanguage() {
  const [url, setUrl] = useState<string>();
  const [isSubmitLoading, setIsSubmitLoading] = useState(false);

  const [signVideo, setSignVideo] = useState<string>();

  const submitForm = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitLoading(true);

    axios
      .get(`${BACKEND_URL}/sign/video?url=${url}`, { responseType: 'blob' })
      .then((response) => {
        console.log(response.data, URL.createObjectURL(response.data));
        setSignVideo(URL.createObjectURL(response.data));
        setIsSubmitLoading(false);
      })
      .catch((err) => {
        console.log(err);
        setIsSubmitLoading(false);
      });
  };

  return (
    <div className="sign-language narration">
      <div className="title">Sign Language</div>
      <form onSubmit={submitForm}>
        <div className="item-group">
          <div className="form-item form-item-long">
            <div className="label">Please enter the audio link here</div>
            <input type="url" value={url} onChange={(event) => setUrl(event.target.value)} />
          </div>
        </div>
        <button className="submit" disabled={isSubmitLoading} type="submit">
          Submit {isSubmitLoading && <CircleNotch />}
        </button>
      </form>
      {!isSubmitLoading && signVideo && (
        <video width="640" height="480" controls src={signVideo}>
          No video element supported
        </video>
      )}
    </div>
  );
}

export default SignLanguage;
