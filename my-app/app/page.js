import Image from 'next/image'

import msg from '../../emails/message0.png'
import msg1 from '../../emails/message1.png'
import msg2 from '../../emails/message2.png'

// components
import Email from '../components/Email.js'

const styles = {
	emailList: {
		display: 'flex',
		flexDirection: 'column',
		alignItems: 'center',
	}
}
  

export default function Home() {
  return (
    <main>
    	<div className='title'>
        	<div>Sup bitch,</div>
			<div>Here's all emails with private positions</div>
      	</div>
      	<div style={styles.emailList}>
			<Email/>
      	</div>
    </main>
  )
}
