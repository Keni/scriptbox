= ru.unix.bsd (2:5090/73) =====================================================
 Msg  : 1 of 12                             
 From : Lev Walkin                          2:5020/400      Thu 22 Jul 04 09:45
 To   : Ivan Poplavsky
 Subj : Re: H���� �������������
===============================================================================
From: Lev Walkin <vlm@netli.com>


Ivan Poplavsky wrote:

> Hello, Lev!
> You wrote to Ivan Poplavsky on Wed, 21 Jul 2004 13:06:23 +0000 (UTC):
> 
> 
>  LW> Ivan Poplavsky wrote:
>  ??>> Hello, All!
>  ??>>
>  ??>> ���� ������ �� ������� �������� Tomcat-4.0.6. ������ ������������
>  ??>> �������� ��-�� �������� ������, �� ��� ���� �ӣ ����� ����� �� ��ϣ�
>  ??>> ����� � ��������� ����������. H���� �����-���� ������������ �������
>  ??>> ����������� �� ��� ����, � �������� ����� ���� ���� �������������
>  ??>> ������.
> 
>  LW> while :; do
>  LW>  curl http://hostname/ || reboot
>  LW>  sleep 5;
>  LW> done
> 
> �������, �� ��� �� ���� ����. ��� ���� ����������� ��������. ������, ���
> ���� ��� ��� ����� ������, � ��������� �����.

��� ���� �������� ������� �� ������ �����...


while :; do
        alive=0
        curl http://hostname1/ && alive=$((alive+1))
        curl http://hostname2/ && alive=$((alive+1))
        curl http://hostname3/ && alive=$((alive+1))
        [ $alive = 0 ] && reboot
        sleep 5;
done


-- 
Lev Walkin
vlm@netli.com

--- ifmail v.2.15dev5.3
 * Origin: Netli, Inc. (2:5020/400)

