import styles from './Email.module.css'
import Image from 'next/image'

import msg from '../../emails/message0.png'
import msg1 from '../../emails/message1.png'
import msg2 from '../../emails/message2.png'

import { Inter } from 'next/font/google'

export const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
})


const people = [{
  id: 0, // Used in JSX as a key
  image: msg
  }, {
  id: 1, // Used in JSX as a key
  image: msg1
  }, {
  id: 2, // Used in JSX as a key
  image: msg2
  }];
 
export default function Email() {

  const listItems = people.map(person =>
    <li key={person.id}>
      <div className={styles.emailTxt}>Email Subtitle</div>
      <Image src={person.image} className={styles.emailPic}/>
    </li>
  );

  return  <ul>{listItems}</ul>;
  
}