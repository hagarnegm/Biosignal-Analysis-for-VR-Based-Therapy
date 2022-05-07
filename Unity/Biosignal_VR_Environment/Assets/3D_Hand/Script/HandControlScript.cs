using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

namespace Sample {
    public class HandControlScript : MonoBehaviour
    {
        [SerializeField] private GameObject _Hand_L;
        [SerializeField] private GameObject _Hand_R;
        private Animator _L_anim;
        private Animator _R_anim;
        private Vector3 _L_InitialPos;
        private Vector3 _R_InitialPos;
        private Quaternion _L_InitialRot;
        private Quaternion _R_InitialRot;
        private Vector3 _TargetPos;
        private Quaternion _TargetRot;
        private float _GroundHight;
        private Coroutine _Cor_L;
        private Coroutine _Cor_R;
        private bool _Wait = false;

        // Socket variables
        public string ip = "127.0.0.1";
        public int port = 25002;

        IPAddress localAdd;
        TcpListener listener;
        TcpClient client;
        Thread newThread;
        bool running;
        int received;
        int previous = 0;
        string[] arr_gest_loop = new string[5];
        int index = 0;

        void Start()
        {
            // sockets threads
            ThreadStart ts = new ThreadStart(GetInfo);
            newThread = new Thread(ts);
            newThread.Start();

            // Hand position
            _L_InitialPos = _Hand_L.transform.position;
            _R_InitialPos = _Hand_R.transform.position;
            _L_InitialRot = _Hand_L.transform.rotation;
            _R_InitialRot = _Hand_R.transform.rotation;
            _L_anim = _Hand_L.GetComponent<Animator>();
            _R_anim = _Hand_R.GetComponent<Animator>();
            _TargetPos = GameObject.Find("Target").transform.position + new Vector3(0, 0, -0.5f);
            _TargetRot = GameObject.Find("Target").transform.rotation;
            _GroundHight = GameObject.Find("Ground").transform.position.y;

        }

        void Update()
        {
            //print("Gestures received is:   " + received);

            if (previous != received)
            {
                TakeAction(received);
                previous = received;
            }

            #region comment
            //if (!_Wait)
            //{
            //    if (Input.GetKeyDown(KeyCode.Q))
            //    {
            //        DAMAGE();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.W))
            //    {
            //        DOWN();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.E))
            //    {
            //        BANG();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.R))
            //    {
            //        HIT();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.T))
            //    {
            //        FLICK();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Y))
            //    {
            //        SHOOT();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.U))
            //    {
            //        SLAP();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.I))
            //    {
            //        HOLD();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.O))
            //    {
            //        PINCH();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.P))
            //    {
            //        CATCH();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.LeftBracket))
            //    {
            //        INDICATE();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.RightBracket))
            //    {
            //        POINTING1();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Backslash))
            //    {
            //        POINTING2();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.A))
            //    {
            //        STOP();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.S))
            //    {
            //        THUMBS_UP();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.D))
            //    {
            //        SNAP();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.F))
            //    {
            //        DICE_ROLL();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.G))
            //    {
            //        SPELL();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.H))
            //    {
            //        PHYCHIC();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.J))
            //    {
            //        HYPNOSIS();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.K))
            //    {
            //        METRONOME();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.L))
            //    {
            //        POKE();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Semicolon))
            //    {
            //        TAP();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Quote))
            //    {
            //        OK();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Z))
            //    {
            //        SWEEP();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.X))
            //    {
            //        DISPEL();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.C))
            //    {
            //        BYE();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.V))
            //    {
            //        SHOO();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.B))
            //    {
            //        KNOCK();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.N))
            //    {
            //        StartCoroutine(Explain());
            //    }
            //    else if (Input.GetKeyDown(KeyCode.M))
            //    {
            //        LISTEN();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Comma))
            //    {
            //        SHOW();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Period))
            //    {
            //        CLAP1();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Slash))
            //    {
            //        CLAP2();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Space))
            //    {
            //        SHRUG();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Minus))
            //    {
            //        AIR_QUOTES();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Alpha0))
            //    {
            //        COUNT0();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Alpha1))
            //    {
            //        COUNT1();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Alpha2))
            //    {
            //        COUNT2();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Alpha3))
            //    {
            //        COUNT3();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Alpha4))
            //    {
            //        COUNT4();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Alpha5))
            //    {
            //        COUNT5();
            //    }
            //    else if (Input.GetKeyDown(KeyCode.Alpha6))
            //    {
            //        GRIP();
            //    }
            //}
            #endregion
        }

        #region sockets
        
        private void TakeAction(int label)
        {

            if (label == 0)
            {
                IDLE();
            }
            else if (label == 1)
            {
                CATCH();
            }
            else if (label == 2)
            {
                THUMBS_UP();
            }
            else if (label == 3)
            {
                COUNT2();
            }
            else if (label == 4)
            {
                STOP();
            }
            else if (label == 5)
            {

            }
        }

        // processing and receiving data from sockets
        void DataReceiver()
        {
            NetworkStream nwStream = client.GetStream();
            byte[] buffer = new byte[client.ReceiveBufferSize];

            // receiving Data
            int dataByte = nwStream.Read(buffer, 0, client.ReceiveBufferSize); // Reading data in Bytes
            string dataString = Encoding.UTF8.GetString(buffer, 0, dataByte); // Converting data to string

            // comparing each five gestures and send only the most appeared one
            arr_gest_loop[index] = dataString;
            index++;
            if (index == 5)
            {
                Dictionary<string, int> dic_count = new Dictionary<string, int>();
                for (int i = 0; i < arr_gest_loop.Length; i++)
                {
                    if (dic_count.ContainsKey(arr_gest_loop[i]))
                    {
                        dic_count[arr_gest_loop[i]] = dic_count[arr_gest_loop[i]] + 1;
                    }
                    else
                    {
                        dic_count.Add(arr_gest_loop[i], 1);
                    }
                }
                int x = 0;
                foreach (var item in dic_count)
                {
                    if (item.Value > x)
                    {
                        x = item.Value;
                        dataString = item.Key;
                    }
                }
                if (dataString == "0")
                {
                    received = 0;
                }
                else if (dataString == "1")
                {
                    received = 1;
                }
                else if (dataString == "2")
                {
                    received = 2;
                }
                else if (dataString == "3")
                {
                    received = 3;
                }
                else if (dataString == "4")
                {
                    received = 4;
                }
                else if (dataString == "5")
                {

                }

                index = 0; 
            }
        }

        // Receive data from sockets
        void GetInfo()
        {
            localAdd = IPAddress.Parse(ip);
            listener = new TcpListener(IPAddress.Any, port);
            listener.Start();

            client = listener.AcceptTcpClient();

            running = true;
            while (running)
            {
                DataReceiver();
            }
        }
        #endregion

        #region play_Gestures
        //_____________________________________________________________________ Play idle
        private void IDLE()
        {
            INITIALIZE_COROUTINE(_Hand_L);
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_L = StartCoroutine(PlayAnimation(_Hand_L, "idle"));
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "idle"));

        }
        //_____________________________________________________________________ Play Damage
        private void DAMAGE()
        {
            INITIALIZE_COROUTINE(_Hand_L);
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_L = StartCoroutine(PlayAnimation(_Hand_L, "damage"));
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "damage"));

        }
        //_____________________________________________________________________ Play Down
        private void DOWN()
        {
            Vector3 pos_l = _Hand_L.transform.position;
            pos_l.y = _GroundHight;
            Vector3 pos_r = _Hand_R.transform.position;
            pos_r.y = _GroundHight;
            INITIALIZE_COROUTINE(_Hand_L);
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_L = StartCoroutine(PosMove(_Hand_L, pos_l, _Hand_L.transform.rotation, "down"));
            _Cor_R = StartCoroutine(PosMove(_Hand_R, pos_r, _Hand_R.transform.rotation, "down"));
        }
        //_____________________________________________________________________ Play Bang
        private void BANG()
        {
            Vector3 pos_l = _Hand_L.transform.position;
            pos_l.y = _GroundHight;
            Vector3 pos_r = _Hand_R.transform.position;
            pos_r.y = _GroundHight;
            INITIALIZE_COROUTINE(_Hand_L);
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_L = StartCoroutine(PosMove(_Hand_L, pos_l, _Hand_L.transform.rotation, "bang"));
            _Cor_R = StartCoroutine(PosMove(_Hand_R, pos_r, _Hand_R.transform.rotation, "bang"));
        }
        //_____________________________________________________________________ Play Hit
        private void HIT()
        {
            Vector3 pos = _TargetPos;
            pos.y = _GroundHight;
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, pos, _TargetRot, "hit"));
        }
        //_____________________________________________________________________ Play Flick
        private void FLICK()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "flick"));
        }
        //_____________________________________________________________________ Play Shoot
        private void SHOOT()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "shoot"));
        }
        //_____________________________________________________________________ Play Slap
        private void SLAP()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "slap"));
        }
        //_____________________________________________________________________ Play Hold
        private void HOLD()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(HoldMove(_Hand_R, _TargetPos, _TargetRot, "hold1", "hold2"));
        }
        //_____________________________________________________________________ Play Pinch
        private void PINCH()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(HoldMove(_Hand_R, _TargetPos, _TargetRot, "pinch1", "pinch2"));
        }
        //_____________________________________________________________________ Play Catch
        private void CATCH()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "catch"));
        }
        //_____________________________________________________________________ Play Come on 1
        private void COME_ON1()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "come_on1"));
        }
        //_____________________________________________________________________ Play Come on 2
        private void COME_ON2()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "come_on2"));
        }
        //_____________________________________________________________________ Play Come on 3
        private void COME_ON3()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "come_on3"));
        }
        //_____________________________________________________________________ Play Come on 4
        private void COME_ON4()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "come_on4"));
        }
        //_____________________________________________________________________ Play Indicate
        private void INDICATE()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "indicate"));
        }
        //_____________________________________________________________________ Play Pointing1
        private void POINTING1()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "pointing1"));
        }
        //_____________________________________________________________________ Play Pointing2
        private void POINTING2()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "pointing2"));
        }
        //_____________________________________________________________________ Play Stop
        private void STOP()
        {
            //INITIALIZE_COROUTINE(_Hand_L);
            INITIALIZE_COROUTINE(_Hand_R);
            //_Cor_L = StartCoroutine(PlayAnimation(_Hand_L, "stop"));
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "stop"));
        }
        //_____________________________________________________________________ Play Thumbs up
        private void THUMBS_UP()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "thumbs_up"));
        }
        //_____________________________________________________________________ Play snap
        private void SNAP()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "snap"));
        }
        //_____________________________________________________________________ Play Dice roll
        private void DICE_ROLL()
        {
            Vector3 pos = _TargetPos;
            pos.y = _GroundHight + 0.5f;
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(HoldMove(_Hand_R, pos, _TargetRot, "dice_roll_loop", "dice_roll"));
        }
        //_____________________________________________________________________ Play Spell
        private void SPELL()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "spell"));
        }
        //_____________________________________________________________________ Play Phychic
        private void PHYCHIC()
        {
            INITIALIZE_COROUTINE(_Hand_L);
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_L = StartCoroutine(PlayAnimation(_Hand_L, "phychic"));
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "phychic"));
        }
        //_____________________________________________________________________ Play Hypnosis
        private void HYPNOSIS()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "hypnosis"));
        }
        //_____________________________________________________________________ Play Metronome
        private void METRONOME()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "metronome"));
        }
        //_____________________________________________________________________ Play Poke
        private void POKE()
        {
            Vector3 pos = _TargetPos;
            pos.y = _GroundHight;
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, pos, _TargetRot, "poke"));
        }
        //_____________________________________________________________________ Play Tap
        private void TAP()
        {
            Vector3 pos = _TargetPos;
            pos.y = _GroundHight;
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, pos, _TargetRot, "tap"));
        }
        //_____________________________________________________________________ Play OK
        private void OK()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(HoldMove(_Hand_R, _Hand_R.transform.position, _Hand_R.transform.rotation, "ok", "ok_loop"));
        }
        //_____________________________________________________________________ Play Sweep
        private void SWEEP()
        {
            Vector3 pos = _TargetPos;
            pos.y = _GroundHight;
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, pos, _TargetRot, "sweep"));
        }
        //_____________________________________________________________________ Play dispel
        private void DISPEL()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "dispel"));
        }
        //_____________________________________________________________________ Play Bye
        private void BYE()
        {
            INITIALIZE_COROUTINE(_Hand_L);
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_L = StartCoroutine(PlayAnimation(_Hand_L, "bye"));
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "bye"));
        }
        //_____________________________________________________________________ Play Shoo
        private void SHOO()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "shoo"));
        }
        //_____________________________________________________________________ Play Knock
        private void KNOCK()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "knock"));
        }
        //_____________________________________________________________________ Play Explain
        private IEnumerator Explain()
        {
            INITIALIZE_COROUTINE(_Hand_L);
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_L = StartCoroutine(PlayAnimation(_Hand_L, "explain1"));
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "explain1"));

            yield return new WaitForSeconds(1.5f);
            INITIALIZE_COROUTINE(_Hand_L);
            _Cor_L = StartCoroutine(PlayAnimation(_Hand_L, "explain3"));

            yield return new WaitForSeconds(1.5f);
            INITIALIZE_COROUTINE(_Hand_L);
            _Cor_L = StartCoroutine(PlayAnimation(_Hand_L, "explain2"));

            yield return new WaitForSeconds(1.0f);
            INITIALIZE_COROUTINE(_Hand_L);
            _Cor_L = StartCoroutine(PlayAnimation(_Hand_L, "explain5"));

            yield return new WaitForSeconds(1.5f);
            Vector3 pos = _TargetPos;
            pos.y = _GroundHight;
            INITIALIZE_COROUTINE(_Hand_L);
            _Cor_L = StartCoroutine(PosMove(_Hand_L, pos, _TargetRot, "explain4"));
        }
        //_____________________________________________________________________ Play Listen
        private void LISTEN()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "listen"));
        }
        //_____________________________________________________________________ Play Show
        private void SHOW()
        {
            Vector3 pos = _TargetPos;
            pos.y = _GroundHight;
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, pos, _TargetRot, "show"));
        }
        //_____________________________________________________________________ Play Clap1
        private void CLAP1()
        {
            Vector3 pos = Vector3.Lerp(_Hand_R.transform.position, _Hand_L.transform.position, 0.5f);
            Quaternion rot = Quaternion.Euler(0, 0, 0);
            INITIALIZE_COROUTINE(_Hand_L);
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_L = StartCoroutine(PosMove(_Hand_L, pos, rot, "clap1_L"));
            _Cor_R = StartCoroutine(PosMove(_Hand_R, pos, rot, "clap1_R"));
        }
        //_____________________________________________________________________ Play Clap2
        private void CLAP2()
        {
            Vector3 pos = Vector3.Lerp(_Hand_R.transform.position, _Hand_L.transform.position, 0.5f);
            Quaternion rot = Quaternion.Euler(0, 0, 0);
            INITIALIZE_COROUTINE(_Hand_L);
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_L = StartCoroutine(PosMove(_Hand_L, pos, rot, "clap2"));
            _Cor_R = StartCoroutine(PosMove(_Hand_R, pos, rot, "clap2"));
        }
        //_____________________________________________________________________ Play Shrug
        private void SHRUG()
        {
            INITIALIZE_COROUTINE(_Hand_L);
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_L = StartCoroutine(PlayAnimation(_Hand_L, "shrug"));
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "shrug"));
        }
        //_____________________________________________________________________ Play Air quotes
        private void AIR_QUOTES()
        {
            INITIALIZE_COROUTINE(_Hand_L);
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_L = StartCoroutine(PlayAnimation(_Hand_L, "air_quotes"));
            _Cor_R = StartCoroutine(PlayAnimation(_Hand_R, "air_quotes"));
        }
        //_____________________________________________________________________ Play Count5
        private void COUNT0()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "count0"));
        }
        //_____________________________________________________________________ Play Count1
        private void COUNT1()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "count1"));
        }
        //_____________________________________________________________________ Play Count2
        private void COUNT2()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "count2"));
        }
        //_____________________________________________________________________ Play Count3
        private void COUNT3()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "count3"));
        }
        //_____________________________________________________________________ Play Count4
        private void COUNT4()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "count4"));
        }
        //_____________________________________________________________________ Play Count5
        private void COUNT5()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "count5"));
        }
        //_____________________________________________________________________ Play Count5
        private void GRIP()
        {
            INITIALIZE_COROUTINE(_Hand_R);
            _Cor_R = StartCoroutine(PosMove(_Hand_R, _TargetPos, _TargetRot, "grip"));
        }

        #endregion

        #region movement and position
        //_____________________________________________________________________ Move Position
        private IEnumerator PosMove(GameObject obj, Vector3 targetPos, Quaternion targetRot, string state_name)
        {
            _Wait = true;
            Vector3 obj_pos = obj.transform.position;
            Quaternion obj_rot = obj.transform.rotation;
            float t = 0;
            while (true)
            {
                if (t > 1)
                {
                    if (obj.name.Substring(5, 1) == "L")
                    {
                        _L_anim.CrossFade(state_name, 0.2f, 0, 0.0f);
                    }
                    else if (obj.name.Substring(5, 1) == "R")
                    {
                        _R_anim.CrossFade(state_name, 0.2f, 0, 0.0f);
                    }
                    yield return new WaitForSeconds(2.0f);
                    if (obj.name.Substring(5, 1) == "L")
                    {
                        _Cor_L = null;
                        _Cor_L = StartCoroutine(InitializePos(obj));
                    }
                    else if (obj.name.Substring(5, 1) == "R")
                    {
                        _Cor_R = null;
                        _Cor_R = StartCoroutine(InitializePos(obj));
                    }
                    yield break;
                }
                t += 1 * Time.deltaTime;
                //obj.transform.position = Vector3.Lerp(obj_pos, targetPos, t);
                //obj.transform.rotation = Quaternion.Lerp(obj_rot, targetRot, t);
                yield return null;
            }
        }
        //_____________________________________________________________________ Move Position - Hold
        private IEnumerator HoldMove(GameObject obj, Vector3 targetPos, Quaternion targetRot, string state_name1, string state_name2)
        {
            _Wait = true;
            Vector3 obj_pos = obj.transform.position;
            Quaternion obj_rot = obj.transform.rotation;
            float t = 0;
            while (true)
            {
                if (t > 1)
                {
                    if (obj.name.Substring(5, 1) == "L")
                    {
                        _L_anim.CrossFade(state_name1, 0.2f, 0, 0.0f);
                    }
                    else if (obj.name.Substring(5, 1) == "R")
                    {
                        _R_anim.CrossFade(state_name1, 0.2f, 0, 0.0f);
                    }

                    yield return new WaitForSeconds(1.0f);

                    if (obj.name.Substring(5, 1) == "L")
                    {
                        _L_anim.CrossFade(state_name2, 0.2f, 0, 0.0f);
                    }
                    else if (obj.name.Substring(5, 1) == "R")
                    {
                        _R_anim.CrossFade(state_name2, 0.2f, 0, 0.0f);
                    }
                    yield return new WaitForSeconds(1.0f);
                    if (obj.name.Substring(5, 1) == "L")
                    {
                        _Cor_L = null;
                        _Cor_L = StartCoroutine(InitializePos(obj));
                    }
                    else if (obj.name.Substring(5, 1) == "R")
                    {
                        _Cor_R = null;
                        _Cor_R = StartCoroutine(InitializePos(obj));
                    }
                    yield break;
                }
                t += 1 * Time.deltaTime;
                //obj.transform.position = Vector3.Lerp(obj_pos, targetPos, t);
                //obj.transform.rotation = Quaternion.Lerp(obj_rot, targetRot, t);
                yield return null;
            }
        }
        //_____________________________________________________________________ Initialize Position
        private IEnumerator InitializePos(GameObject obj)
        {
            Vector3 obj_pos = Vector3.zero;
            Quaternion obj_rot = Quaternion.Euler(0, 0, 0);
            Vector3 end_pos = Vector3.zero;
            Quaternion end_rot = Quaternion.Euler(0, 0, 0);

            //if (obj.name.Substring(5, 1) == "L")
            //{
            //    obj_pos = _Hand_L.transform.position;
            //    obj_rot = _Hand_L.transform.rotation;
            //    end_pos = _L_InitialPos;
            //    end_rot = _L_InitialRot;
            //    _L_anim.CrossFade("idle", 0.2f, 0, 0.0f);
            //}
            //else if (obj.name.Substring(5, 1) == "R")
            //{
            //    obj_pos = _Hand_R.transform.position;
            //    obj_rot = _Hand_R.transform.rotation;
            //    end_pos = _R_InitialPos;
            //    end_rot = _R_InitialRot;
            //    _R_anim.CrossFade("idle", 0.2f, 0, 0.0f);
            //}

            float t = 0;
            while (true)
            {
                if (t > 1)
                {
                    _Wait = false;
                    yield break;
                }
                t += 1 * Time.deltaTime;

                //obj.transform.position = Vector3.Lerp(obj_pos, end_pos, t);
                //obj.transform.rotation = Quaternion.Lerp(obj_rot, end_rot, t);

                yield return null;
            }
        }
        //_____________________________________________________________________ Play Animation
        private IEnumerator PlayAnimation(GameObject obj, string state_name)
        {
            _Wait = true;
            if (obj.name.Substring(5, 1) == "L")
            {
                _L_anim.CrossFade(state_name, 0.2f, 0, 0.0f);
            }
            else if (obj.name.Substring(5, 1) == "R")
            {
                _R_anim.CrossFade(state_name, 0.2f, 0, 0.0f);
            }
            yield return new WaitForSeconds(1.5f);
            //if (obj.name.Substring(5, 1) == "L")
            //{
            //    _L_anim.CrossFade("idle", 0.2f, 0, 0.0f);
            //    _Cor_L = null;
            //    _Cor_L = StartCoroutine(InitializePos(obj));
            //}
            //else if (obj.name.Substring(5, 1) == "R")
            //{
            //    _R_anim.CrossFade("idle", 0.2f, 0, 0.0f);
            //    _Cor_R = null;
            //    _Cor_R = StartCoroutine(InitializePos(obj));
            //}
        }
        //_____________________________________________________________________ Initialize Coroutine
        private void INITIALIZE_COROUTINE(GameObject obj)
        {
            try
            {
                if (obj.name.Substring(5, 1) == "L")
                {
                    StopCoroutine(_Cor_L);
                }
                else if (obj.name.Substring(5, 1) == "R")
                {
                    StopCoroutine(_Cor_R);
                }
            }
            catch (System.NullReferenceException)
            {
                // None method
            }
            if (obj.name.Substring(5, 1) == "L")
            {
                _Cor_L = null;
            }
            else if (obj.name.Substring(5, 1) == "R")
            {
                _Cor_R = null;
            }
        }
        #endregion
    }
}