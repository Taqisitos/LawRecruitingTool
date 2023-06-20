import styles from './Email.module.css'
import Image from 'next/image'

import { Inter } from 'next/font/google'

export const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
})
 
export default function Email({emailPic}) {
  return (
    <>
        <div className={styles.emailTxt}>Email subtitle</div>
        <Image src={emailPic} className={styles.emailPic}/>
    </>
  )
}